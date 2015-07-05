import errors
import logging
import json
import base64
import urllib
import Objects.UserObj as user_lib
from google.appengine.ext import ndb
from Crypto.Cipher import AES
import webapp2
import urlparse

def validate_data(request):
    dictionary = {}
    if "json" in request.headers['Content-Type']:
        dictionary = json.loads(request.body)
        try:
            # x = dictionary["location"]
            dictionary["location"] = "GeomFromText('" + dictionary["location"] + "')"
        except KeyError:
            pass
        logging.info("body:  %s", request.body)
    else:
        for key in request.params:
            # if not request.get(key):
            # error = errors.Error("data::Invalid Data")
            #     logging.error(error.message())
            #     return error, None
            if key.lower() == "location":
                dictionary[key.lower()] = "GeomFromText('" + request.get(key) + "')"
            else:
                dictionary[key.lower()] = request.get(key)
    for key, value in dictionary.iteritems():
        if not value:
            error = errors.Error("data::Invalid Data")
            logging.error(error.message())
            return error, None
    # logging.info(dictionary)
    return None, dictionary

# Encryption

# Output = Base64Encode(Encrypt(Raw message(UID) + server's secret))

# The encrypt function first encrpyts the message with our server secret key
# Then, it base 64 encodes the encrpyted message (the ciphertext), so that
# the return string contains no special/escape character.

auth_secret_msg = 'AlexAbyxious1234'


def encrypt(message):
    obj = AES.new(auth_secret_msg)
    ciphertext = obj.encrypt(message)
    return urllib.quote(str(ciphertext))


def decrypt(message):
    ciphertext = urllib.unquote(message)
    obj = AES.new(auth_secret_msg)
    raw_msg = obj.decrypt(ciphertext)
    return str(raw_msg)


def json_obj(obj):
    data = {}
    for x in dir(obj):
        if x != "id":
            data[x] = getattr(obj, x)
        else:
            if obj.id:
                data["id"] = obj.id
    return data


def dictionarize(obj):
    if not hasattr(obj, "__dict__"):
        return obj
    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue
        if isinstance(val, list):
            element = []
            for item in val:
                element.append(dictionarize(item))
        else:
            element = dictionarize(val)
        result[key] = element
    return result


def process_cookie(request, response):
    cookie_value = request.cookies.get('FDUP')

    if cookie_value:
        user_id = decrypt(str(cookie_value))
        key = ndb.Key(user_lib.UserModel, int(user_id))
        ent = key.get()
        if ent:
            temp_user = user_lib.User(username=ent.username, password=ent.password, ID=str(user_id),
                                      profile=json.loads(ent.profile))
            return True, temp_user
        else:
            response.status = 401
            return False, None
    else:
        response.status = 401
        return False, None


def generate_json(request, uid, method, data, error):
    url_string = str(request.url)
    url_obj = urlparse.urlparse(url_string)
    # str.split returns a list of strings. Google search python str.split for more detail.
    subdirs = str(url_obj.path).split('/')
    dictionary = {
        'head': {
            'uid': uid,
            'type': subdirs[1],
            'url': request.url,
            'method': method
        },
        'data': data,
        'error': error
    }
    return json.dumps(dictionary)


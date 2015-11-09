import errors
import logging
import json
import urllib
from Crypto.Cipher import AES
import urlparse

FIIDUP_COOKIE = 'FDUP'

def parse_request(request):
    url_string = str(request.url)
    url_obj = urlparse.urlparse(url_string)

def validate_data(request):
    dictionary = {}
    logging.info(request.method)
    content_type = request.headers['Content-Type'].split(';')[0]
    logging.info(content_type)
    if request.method == 'POST' or request.method == 'PUT':
        if "json" in content_type:
            dictionary = json.loads(request.body)
            try:
                dictionary["location"] = "GeomFromText('" + dictionary["location"] + "')"
            except KeyError:
                pass
            logging.info("body:  %s", request.body)
        elif "x-www-form-urlencoded" in content_type:
            for key in request.params:
                # if not request.get(key):
                # error = errors.Error("data::Invalid Data")
                #     logging.error(error.message())
                #     return error, None
                if key.lower() == "location":
                    dictionary[key.lower()] = "GeomFromText('" + request.get(key) + "')"
                else:
                    dictionary[key.lower()] = request.get(key)
        elif not content_type:
            return None, dictionary
        else:
            error = errors.Error("headers::Invalid Header:Content-Type")
            logging.error(error.message())
            return error, None
    elif request.method == 'GET':
        for key in request.params:
            if key.lower() == "location":
                dictionary[key.lower()] = "GeomFromText('" + request.get(key) + "')"
            else:
                dictionary[key.lower()] = request.get(key)
    elif request.method == 'DELETE':
        # check the data for DELETE. Have to add the function
        pass
    else:
        error = errors.Error("method::Not Allowed")
        logging.error(error.message())
        return error, None

    if dictionary :
        for key, value in dictionary.iteritems():
            if not value:
                error = errors.Error("data::Invalid Data")
                logging.error(error.message())
                return error, None
    else:
        error = errors.Error("data::Empty Data")
        logging.error(error.message())
        return error, None
    return None, dictionary

# Encryption

# Output = Base64Encode(Encrypt(Raw message(UID) + server's secret))

# The encrypt function first encrpyts the message with our server secret key
# Then, it base 64 encodes the encrpyted message (the ciphertext), so that
# the return string contains no special/escape character.

auth_secret_msg = 'AlexAbyxious1234'


def encrypt(message):
    obj = AES.new(auth_secret_msg)
    ciphertext = obj.encrypt(str(message).zfill(16))
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

def process_cookie(request):
    user_id = None
    authenticated = False
    cookie_value = request.cookies.get(FIIDUP_COOKIE)
    if cookie_value:
        user_id = int(decrypt(str(cookie_value)))
        # TODO: checks if this user_id exists in the database
        user_exist = True
        if user_id:
            authenticated = True
    return authenticated, user_id

def generate_json(request, uid, method, data, error):
    url_string = str(request.url)
    logging.info(url_string)
    url_obj = urlparse.urlparse(url_string)
    # str.split returns a list of strings. Google search python str.split for more detail.
    subdirs = str(url_obj.path).split('/')
    logging.info(subdirs)
    dictionary = {
        'head': {
            'uid': uid,
            'type': subdirs[1],
            'url': url_string,
            'method': method
        },
        'data': data,
        'error': error
    }
    logging.info(json.dumps(dictionary))
    return json.dumps(dictionary)

def fail_blacklist(blacklist, params):
    for param in params:
        if param in blacklist:
            return True
    return False

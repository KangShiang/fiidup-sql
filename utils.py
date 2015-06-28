import errors
import logging
import json


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
            #     error = errors.Error("data::Invalid Data")
            #     logging.error(error.message())
            #     return error, None
            if key.lower() == "location":
                dictionary[key.lower()] = "GeomFromText('" + request.get(key) + "')"
            else:
                dictionary[key.lower()] = request.get(key)
    for key, value in dictionary.iteritems():
        if not value :
            error = errors.Error("data::Invalid Data")
            logging.error(error.message())
            return error, None
    logging.info(dictionary)
    return None, dictionary
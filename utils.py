import errors
import logging


def validate_data(request):
    dictionary = {}
    for key in request.params:
        if not request.get(key):
            error = errors.Error("data::Invalid Data")
            logging.error(error.message())
            return error, None
        if key.lower() == "location":
            dictionary[key.lower()] = "GeomFromText('" + request.get(key) + "')"
        else:
            dictionary[key.lower()] = request.get(key)
    logging.info(dictionary)
    return None, dictionary
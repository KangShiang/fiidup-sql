import errors
import logging


def validate_data(request):
    dictionary = {}
    for key in request.params:
        if not request.get(key):
            error = errors.Error("Invalid Data")
            logging.error(error.message())
            return error, None

        dictionary[key.lower()] = request.get(key)
    logging.info(dictionary)
    return None, dictionary
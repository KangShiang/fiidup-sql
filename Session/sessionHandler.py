import utils
import json
import webapp2

def delete_session(handler, params):
    # TODO: Need to be checked
    handler.response.set_cookie(handler.app.config.get('cookie_name'),
                                str(utils.encrypt(temp_user.id)), max_age=-1,
                                path=handler.app.config.get('cookie_path'),
                                domain=handler.app.config.get('cookie_domain'),
                                secure=handler.app.config.get('secure_cookie'))

def get_session(handler, params):
    authenticated, temp_user = utils.process_cookie(handler.request, handler.response)
    if not authenticated:
        return

    if temp_user:
        handler.response.headers['Content-Type'] = 'application/json'
        dictionary = {
                'head':{
                    'id': temp_user.id,
                    'type': 'session',
                    'username':temp_user.username,
                },
                'data' : utils.dictionarize(temp_user),
                'error':None
        }
        handler.response.write(json.dumps(dictionary))
    else:
        handler.response.write('Cookie Not Found')

def post_session(handler, params):
    handler.response.out.write("Post to session" + " and Param =" + str(params))
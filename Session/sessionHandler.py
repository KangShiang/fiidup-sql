import sql
import utils
from datetime import datetime, timedelta


def delete_session(handler):
    data = None
    error = None
    authenticated, user_id = utils.process_cookie(handler.request)
    if authenticated:
        handler.response.delete_cookie(utils.FIIDUP_COOKIE)
        data = {'session': 'ended'}
    else:
        error = 'Session does not exist'
        handler.response.status = 401
    handler.response.out.write(utils.generate_json(handler.request, user_id, "DELETE", data, error))

def get_session(handler):
    data = None
    error = None
    authenticated, user_id = utils.process_cookie(handler.request)
    if authenticated and user_id:
        data = {'session': 'valid'}
    else:
        error = 'Session does not exist'
        handler.response.status = 401
    handler.response.out.write(utils.generate_json(handler.request, user_id, "GET", data, error))

def post_session(handler, params):
    data = None
    error = None
    cursor = sql.db.cursor()
    authenticated, user_id = utils.process_cookie(handler.request)
    if authenticated:
        error = 'Session already exists'
        handler.response.status = 403
    else:
        username = params['username']
        password = params['password']
        condition = {"username": str(username), "password": str(password)}
        query_string = sql.get_retrieve_query_string(table="person", params=['user_id'], cond=condition)
        cursor.execute(query_string)
        uid = cursor.fetchall()
        if uid:
            uid = uid[0][0]
            expiry = datetime.today() + timedelta(days=365)
            cookie = str(utils.encrypt(uid))
            handler.response.set_cookie(utils.FIIDUP_COOKIE, cookie, expires=expiry,
                                        path=handler.app.config.get('cookie_path'),
                                        domain=handler.app.config.get('cookie_domain'),
                                        secure=handler.app.config.get('secure_cookie'))
            data = {'user_id': uid,
                    'expires': expiry.isoformat(' ')}
        else:
            error = 'User does not exist'
            handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, user_id, "POST", data, error))

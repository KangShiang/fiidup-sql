import MySQLdb
import sql
import json
import utils
import logging

def get_follower(handler, id, params):
    data = None
    error = None
    cursor = sql.db.cursor()
    # get this user id
    user_id = utils.get_user(handler.request, handler.response)
    # obtain all followers of this user by default
    cond = {'user_id': str(user_id)}
    if user_id is None:
        cursor.close()
        error = "You do not have a user id. Good bye..."
        return data, error
    if id:
        # obtain all followers of the user with this id
        cond = {'user_id': str(id)}
    try:
        query = sql.get_retrieve_query_string(table='follower', cond=cond)
        cursor.execute(query)
        follower_dict = cursor.fetchall()[0][1]
        follower_dict = json.loads(cursor.fetchall()[0][1]) if follower_dict is not None else {}
        data = follower_dict
    except MySQLdb.Error, e:
        try:
            logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            logging.error("MySQL Error: %s" % str(e))
            error = "MySQL Error: %s" % str(e)
        handler.response.status = 403

    cursor.close()
    logging.info(data)
    return data, error

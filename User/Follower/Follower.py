import MySQLdb
import sql
import json
import utils
import logging

def get_follower(handler, this_user, target_user):
    # User id is always passed in as id
    data = None
    error = None
    cursor = sql.db.cursor()
    cond = {'user_id': target_user}
    try:
        query = sql.get_retrieve_query_string(table='follower', cond=cond)
        cursor.execute(query)
        follower_dict = cursor.fetchall()[0][1]
        follower_dict = json.loads(follower_dict) if follower_dict is not None else {}
        data = follower_dict
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        handler.response.status = 403
    cursor.close()
    logging.info(data)
    handler.response.out.write(utils.generate_json(handler.request, this_user, "GET", data, error))

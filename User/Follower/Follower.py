import MySQLdb
import sql
import utils

def get_follower(handler, this_user, target_user):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        query, keys = sql.get_follow_join_user_query(target_user, 'follower')
        cursor.execute(query)
        data = []
        for values in cursor.fetchall():
            values = dict(zip(keys, values))
            data.append(values)
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "GET", data, error))

import MySQLdb
import sql
import utils

def put_following(handler, this_user, params):
    data = None
    error = None
    cursor = sql.db.cursor()
    target_user = params['user_id']
    if target_user == str(this_user):
        error = 'Don\'t try to be your own shadow! Follow someone else please...'
    else:
        try:
            params = {'follower': this_user, 'following': target_user}
            query = sql.get_insert_query_string('follow', params)
            cursor.execute(query)
            # increment fiiding and fiider counts
            param = {'fiiding_count': 'fiiding_count + 1'}
            query = sql.get_modify_query_string(table='person', params=param, primary_key='user_id', id=this_user)
            cursor.execute(query)
            param = {'fiider_count': 'fiider_count + 1'}
            query = sql.get_modify_query_string(table='person', params=param, primary_key='user_id', id=target_user)
            cursor.execute(query)
            sql.db.commit()
            data = {'following': target_user}
        except MySQLdb.Error, e:
            error = sql.get_sql_error(e)
            sql.db.rollback()
            handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "PUT", data, error))

def get_following(handler, this_user, target_user):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        query, keys = sql.get_follow_join_user_query(target_user, 'following')
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

def delete_following(handler, this_user, target_user):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        # TODO: remove check when sql trigger is implemented - check so that count is not decremented if fail
        condition = {'follower': this_user, 'following': target_user}
        query_string = sql.get_retrieve_query_string(table="follow", cond=condition, limit=1)
        cursor.execute(query_string)
        if cursor.fetchall():
            query = sql.get_delete_query_string('follow', condition)
            cursor.execute(query)
            # decrement fiiding and fiider counts
            param = {'fiiding_count': 'fiiding_count - 1'}
            query = sql.get_modify_query_string(table='person', params=param, primary_key='user_id', id=this_user)
            cursor.execute(query)
            param = {'fiider_count': 'fiider_count - 1'}
            query = sql.get_modify_query_string(table='person', params=param, primary_key='user_id', id=target_user)
            cursor.execute(query)
            sql.db.commit()
            data = {'following': target_user}
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        sql.db.rollback()
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "DELETE", data, error))

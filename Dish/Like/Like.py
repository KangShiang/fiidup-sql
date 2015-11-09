import sql
import utils
import MySQLdb

def get_like(handler, this_user, target_dish):
    data = None
    error = None
    cursor = sql.db.cursor()
    condition = {'dish_id': '= %s' % target_dish}
    query_string, extra_param = sql.get_table_join_user_query('dish_like', cond=condition)
    try:
        cursor.execute(query_string)
        data = []
        keys = sql.get_column_names('dish_like')
        keys.extend(extra_param)
        for values in cursor.fetchall():
            values = dict(zip(keys, values))
            data.append(values)
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "GET", data, error))

def delete_like(handler, this_user, target_dish):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        # TODO: remove check when sql trigger is implemented - check so that count is not decremented if fail
        condition = {'dish_id': target_dish, 'user_id': this_user}
        query_string = sql.get_retrieve_query_string(table="dish_like", cond=condition, limit=1)
        cursor.execute(query_string)
        if cursor.fetchall():
            query = sql.get_delete_query_string('dish_like', condition)
            cursor.execute(query)
            # decrement like_count in dish table
            param = {'like_count': 'like_count - 1'}
            query = sql.get_modify_query_string(table='dish', params=param, primary_key='dish_id', id=target_dish)
            cursor.execute(query)
            sql.db.commit()
            data = condition
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        sql.db.rollback()
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "DELETE", data, error))

def post_like(handler, this_user, target_dish, req_params):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        params = {'dish_id': target_dish, 'user_id': this_user}
        query = sql.get_insert_query_string('dish_like', params)
        cursor.execute(query)
        # increment like_count in dish table
        param = {'like_count': 'like_count + 1'}
        query = sql.get_modify_query_string(table='dish', params=param, primary_key='dish_id', id=target_dish)
        cursor.execute(query)
        sql.db.commit()
        data = params
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        sql.db.rollback()
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "POST", data, error))

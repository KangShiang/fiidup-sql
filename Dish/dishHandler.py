import MySQLdb
import sql
import time
import utils
from copy import deepcopy

def get_dish(handler, this_user, target_dish):
    data = None
    error = None
    count = 10
    cursor = sql.db.cursor()
    if target_dish:
        condition = {"dish_id": '= %s' % target_dish}
        query_string, extra_param = sql.get_dish_get_query(limit=1, cond=condition)
    else:
        condition = deepcopy(dict(handler.request.GET))
        if 'count' in condition:
            count = condition['count']
            del condition['count']
        query_string, extra_param = sql.get_dish_get_query(limit=count, cond=condition)
    try:
        cursor.execute(query_string)
        data = []
        keys = sql.get_column_names('dish')
        keys.extend(extra_param)
        for values in cursor.fetchall():
            values = dict(zip(keys, values))
            data.append(values)
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "GET", data, error))

def delete_dish(handler, this_user, target_dish):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        # check if the dish was posted by this user
        condition = {"user_id": this_user, "dish_id": target_dish}
        query_string = sql.get_retrieve_query_string(table="dish", cond=condition, limit=1)
        cursor.execute(query_string)
        if cursor.fetchall():
            condition = {"dish_id": target_dish}
            query = sql.get_delete_query_string('dish', condition)
            cursor.execute(query)
            sql.db.commit()
            data = {'dish_id': target_dish}
        else:
            handler.response.status = 401
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        sql.db.rollback()
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "DELETE", data, error))

def post_dish(handler, this_user, params):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        params['user_id'] = this_user
        params['posted_time'] = float('%.2f' % time.time())
        query = sql.get_insert_query_string("dish", params)
        cursor.execute(query)
        sql.db.commit()
        data = params
        data['dish_id'] = sql.get_last_inserted_pkey(cursor)
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        sql.db.rollback()
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "POST", data, error))

def put_dish(handler, this_user, target_dish, req_params):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        # check if the dish was posted by this user
        condition = {"user_id": this_user, "dish_id": target_dish}
        query_string = sql.get_retrieve_query_string(table="dish", cond=condition, limit=1)
        cursor.execute(query_string)
        if cursor.fetchall():
            query_string = sql.get_modify_query_string("dish", req_params, "dish_id", target_dish)
            cursor.execute(query_string)
            sql.db.commit()
            data = req_params
        else:
            handler.response.status = 401
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        sql.db.rollback()
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "PUT", data, error))

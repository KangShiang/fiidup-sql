import MySQLdb
import sql
import utils
import time
from copy import deepcopy

def get_comment(handler, this_user, target_dish):
    data = None
    error = None
    count = 10
    cursor = sql.db.cursor()
    condition = deepcopy(dict(handler.request.GET))
    if 'count' in condition:
        count = condition['count']
        del condition['count']
    condition['dish_id'] = '= %s' % target_dish
    query_string, extra_param = sql.get_table_join_user_query('comment', cond=condition, limit=count)
    try:
        cursor.execute(query_string)
        data = []
        keys = sql.get_column_names('comment')
        keys.extend(extra_param)
        for values in cursor.fetchall():
            values = dict(zip(keys, values))
            data.append(values)
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "GET", data, error))

def delete_comment(handler, this_user, target_dish, target_comment=None):
    data = None
    error = None
    cursor = sql.db.cursor()
    if not target_comment:
        error = 'Comment to be deleted is not specified'
        handler.response.status = 403
    else:
        try:
            # check if the comment was posted by this user for the dish
            condition = {"comment_id": target_comment, "dish_id": target_dish, "user_id": this_user}
            query_string = sql.get_retrieve_query_string(table="comment", cond=condition, limit=1)
            cursor.execute(query_string)
            if cursor.fetchall():
                condition = {"comment_id": target_comment}
                query = sql.get_delete_query_string('comment', condition)
                cursor.execute(query)
                # decrement comment_count in dish table
                param = {'comment_count': 'comment_count - 1'}
                query = sql.get_modify_query_string(table='dish', params=param, primary_key='dish_id', id=target_dish)
                cursor.execute(query)
                sql.db.commit()
                data = {'comment_id': target_comment}
            else:
                handler.response.status = 401
        except MySQLdb.Error, e:
            error = sql.get_sql_error(e)
            sql.db.rollback()
            handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "DELETE", data, error))

def post_comment(handler, this_user, target_dish, req_params):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        req_params['dish_id'] = target_dish
        req_params['user_id'] = this_user
        req_params['posted_time'] = float('%.2f' % time.time())
        query = sql.get_insert_query_string('comment', req_params)
        cursor.execute(query)
        data = req_params
        data['comment_id'] = sql.get_last_inserted_pkey(cursor)
        # increment comment_count in dish table
        param = {'comment_count': 'comment_count + 1'}
        query = sql.get_modify_query_string(table='dish', params=param, primary_key='dish_id', id=target_dish)
        cursor.execute(query)
        sql.db.commit()
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        sql.db.rollback()
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "POST", data, error))

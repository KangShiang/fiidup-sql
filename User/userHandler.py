import sql
import utils
import MySQLdb
import logging

def get_user(handler, this_user, target_user):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        condition = {"user_id": target_user}
        query_string = sql.get_retrieve_query_string(table="person", cond=condition)
        cursor.execute(query_string)
        for values in cursor.fetchall():
            new_values = []
            for x in values:
                new_values.append(x)
            keys = sql.get_column_names('person')
            data = dict(zip(keys, new_values))
            del data['password']
            logging.info(data)
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "GET", data, error))

def put_user(handler, this_user, params):
    """
    Modifies this user's information in the person database
    """
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        query_string = sql.get_modify_query_string("person", params, "user_id", str(this_user))
        cursor.execute(query_string)
        sql.db.commit()
        data = params
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "PUT", data, error))

def post_user(handler, this_user, params):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        query = sql.get_insert_query_string("person", params)
        cursor.execute(query)
        sql.db.commit()
        data = params
        data['user_id'] = sql.get_last_inserted_pkey(cursor)
        handler.response.status = 200
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        sql.db.rollback()
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "POST", data, error))

def delete_user(handler, this_user):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        query = sql.get_delete_query_string('person', 'user_id', this_user)
        cursor.execute(query)
        sql.db.commit()
        data = {'user_id': this_user,
                'session': 'ended'}
        # delete session
        handler.response.delete_cookie(utils.FIIDUP_COOKIE)
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        sql.db.rollback()
        handler.response.status = 403
    cursor.close()
    handler.response.out.write(utils.generate_json(handler.request, this_user, "DELETE", data, error))

import webapp2
import MySQLdb
import sql as fiidup_sql
import logging
import json
import utils

def put_dish(handler, id, params):
    error = None
    if id:
        cursor = fiidup_sql.db.cursor()
        try:
            query_string = fiidup_sql.get_modify_query_string("dish", params, "dish_id", id)
            cursor.execute(query_string)
            fiidup_sql.db.commit()
            return params, error
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)

            handler.response.status = 403
            return None, error
        cursor.close()
    else:
        error = "ID not found"
        handler.response.status = 403
        return None, error


def get_dish(handler, id, params):
    error = None
    if id:
        cursor = fiidup_sql.db.cursor()
        try:
            condition = [{"dish_id": "=%s" % id}]
            query_string = fiidup_sql.get_retrieve_query_string(table="dish", cond=condition, limit=1)
            cursor.execute(query_string)
            dish = cursor.fetchall()[0]
            return dish, error
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            handler.response.status = 403
            return None, error
        cursor.close()
        handler.response.out.write(utils.generate_json(handler.request, id, "GET", params, None))
    else:
        handler.response.out.write("Get to dish" + " and Param =" + str(params))


def post_dish(handler, id, params):
    if id:
        handler.response.out.write("Post to dish " + "when id = " + id + " and Param =" + str(params))
    else:
        cursor = fiidup_sql.db.cursor()
        try:
            query = fiidup_sql.get_insert_query_string("dish", params)
            cursor.execute(query)
            fiidup_sql.db.commit()
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
        handler.response.out.write(json.dumps(params))
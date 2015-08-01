import webapp2
import MySQLdb
import sql as fiidup_sql
import logging
import cgi

def put_dish(handler, id, params):
    data = None
    error = None
    cursor = fiidup_sql.db.cursor()
    if id:
        try:
            query_string = fiidup_sql.get_modify_query_string("dish", params, "dish_id", id)
            cursor.execute(query_string)
            fiidup_sql.db.commit()
            data = params
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                if e.args[0] == 1054:
                    error = "Invalid Argument"
                else:
                    error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            handler.response.status = 403
    else:
        error = "ID not found"
        handler.response.status = 403
    cursor.close()
    return data, error

def get_dish(handler, id, params):
    error = None
    dish = None
    cursor = fiidup_sql.db.cursor()
    if id:
        try:
            condition = {"dish_id": id}
            query_string = fiidup_sql.get_retrieve_query_string(table="dish", cond=condition, limit=1)
            cursor.execute(query_string)
            try:
                values = cursor.fetchall()
                new_values = []
                for x in values:
                    try:
                        int(x)
                        new_values.append(x)
                    except ValueError:
                        new_values.append(cgi.escape(x))
                cursor.execute("DESCRIBE %s" % "dish;")
                keys = [x[0] for x in cursor.fetchall()]
                dish = dict(zip(keys, new_values))
                logging.info(dish)
            except IndexError:
                pass
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                if e.args[0] == 1054:
                    error = "Invalid Argument"
                else:
                    error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            handler.response.status = 403
    else:
        if params.get("count"):
            count = params.get("count")
            del params['count']
        else:
            count = 10
        logging.info("GET DISH WITH COUNT", count)
        try:
            condition = params
            query_string = fiidup_sql.get_retrieve_numeric_query_string(table="dish", cond=condition, limit=count)
            cursor.execute(query_string)
            try:
                values = cursor.fetchall()
                cursor.execute("DESCRIBE %s" % "dish;")
                keys = [x[0] for x in cursor.fetchall()]
                logging.info(values)
                dish_list = []
                for list in values:
                    new_values = []
                    for x in list:
                        try:
                            int(x)
                            new_values.append(x)
                        except ValueError:
                            new_values.append(cgi.escape(x))
                    dish = dict(zip(keys, new_values))
                    dish_list.append(dish)
                logging.info(dish_list)
                dish = dish_list
            except IndexError:
                pass
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                if e.args[0] == 1054:
                    error = "Invalid Argument"
                else:
                    error = "Invalid Syntax"
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            handler.response.status = 403
    cursor.close()
    return dish, error

def post_dish(handler, id, params):
    data = None
    error = None
    cursor = fiidup_sql.db.cursor()
    if id:
        error = "Key specified for a POST request"
        handler.response.status = 403
    else:
        try:
            query = fiidup_sql.get_insert_query_string("dish", params)
            cursor.execute(query)
            fiidup_sql.db.commit()
            data = params
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            handler.response.status = 403
    cursor.close()
    return data, error

def delete_dish(handler, id, params):
    # id represents dish_id
    data = None
    error = None
    cursor = fiidup_sql.db.cursor()
    if id:
        try:
            query = fiidup_sql.get_delete_query_string('dish', 'dish_id', id)
            cursor.execute(query)
            fiidup_sql.db.commit()
            data = {'dish_id': id}
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            fiidup_sql.db.rollback()
            handler.response.status = 403
    else:
        error = "Key not found"
        handler.response.status = 403
    cursor.close()
    return data, error

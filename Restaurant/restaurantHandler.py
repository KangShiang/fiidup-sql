import webapp2
import MySQLdb
import sql as fiidup_sql
import logging
import json
import cgi
import utils

def put_restaurant(handler, id, params):
    error = None
    if id:
        cursor = fiidup_sql.db.cursor()
        try:
            query_string = fiidup_sql.get_modify_query_string("restaurant", params, "restaurant_id", id)
            cursor.execute(query_string)
            fiidup_sql.db.commit()
            return params, error
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                if e.args[0] == 1054:
                    handler.response.status = 403
                    error = "Invalid Argument"
                    return params, error
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

def get_restaurant(handler, id, params):
    error = None
    restaurant = []
    if id:
        cursor = fiidup_sql.db.cursor()
        try:
            condition = {"restaurant_id": id}
            query_string = fiidup_sql.get_retrieve_query_string(table="restaurant", cond=condition, limit=1)
            cursor.execute(query_string)
            try:
                values = cursor.fetchall()
                new_values = []
                for x in values:
                    try:
                        int(x)
                        new_values.append(x)
                    except (ValueError):
                        new_values.append(cgi.escape(x))
                cursor.execute("DESCRIBE %s" % "dish;")
                keys = [x[0] for x in cursor.fetchall()]
                restaurant = dict(zip(keys, new_values))
                logging.info(restaurant)
                return restaurant, error
            except IndexError:
                return restaurant, None
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                if e.args[0] == 1054:
                    error = "Invalid Argument"
                    return None , error
                error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            handler.response.status = 403
            return None, error
        cursor.close()
    else:
        cursor = fiidup_sql.db.cursor()
        if params.get("count"):
            count = params.get("count")
            del params['count']
        else:
            count = 10

        logging.info("GET RETAURANT WITH COUNT", count)

        try:
            condition = params
            query_string = fiidup_sql.get_retrieve_numeric_query_string(table="restaurant", cond=condition, limit=count)
            logging.info(query_string)
            cursor.execute(query_string)
            try:
                values = cursor.fetchall()
                cursor.execute("DESCRIBE %s" % "restaurant;")
                keys = [x[0] for x in cursor.fetchall()]
                restaurant_list = []
                logging.info(values)
                for list in values:
                    logging.info("List:%s", list)
                    new_values = []
                    for x in list:
                        new_values.append(x)
                    restaurant = dict(zip(keys, new_values))
                    restaurant_list.append(restaurant)
                logging.info(restaurant_list)
                return restaurant_list, error
            except IndexError:
                return restaurant, None
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                if e.args[0] == 1054:
                    error = "Invalid Argument"
                    return None , error
                error = "Invalid Syntax"
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            handler.response.status = 403
            return None, error
        cursor.close()
        # handler.response.out.write("Get to dish" + " and Param =" + str(params))

def post_restaurant(handler, id, params):
    data = None
    error = None
    cursor = fiidup_sql.db.cursor()
    if id:
        error = "Key specified for a POST request"
        handler.response.status = 403
    else:
        try:
            query = fiidup_sql.get_insert_query_string("restaurant", params)
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

def delete_restaurant(handler, id, params):
    logging.info(id)
    data = None
    error = None

    cursor = fiidup_sql.db.cursor()
    try:
        query = fiidup_sql.get_delete_query_string("restaurant", "restaurant_id", id)
        cursor.execute(query)
        fiidup_sql.db.commit()
        data = {'status': 'Success'}
        return data, error
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
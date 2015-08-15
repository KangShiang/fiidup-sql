import logging
import sql as fiidup_sql

def put_keep(handler, id, params):
    if id:
        result = None
        error = None
        cursor = fiidup_sql.db.cursor()
        condition = {"restaurant_id": id}
        query_string = fiidup_sql.get_retrieve_query_string(table="restaurant_keep", cond=condition, limit=1)
        cursor.execute(query_string)
        try:
            values = cursor.fetchall()
            new_values = []
            for value in values:
                for x in value:
                    try:
                        new_values.append(x)
                    except (ValueError):
                        new_values.append(cgi.escape(x))
            cursor.execute("DESCRIBE %s" % "restaurant_keep;")
            keys = [x[0] for x in cursor.fetchall()]
            restaurant_keep = dict(zip(keys, new_values))
            if restaurant_keep.get('user_id') != "":
                restaurant_keep['user_id'] = restaurant_keep.get('user_id').split(',')
            else:
                restaurant_keep['user_id'] = []
            logging.info(restaurant_keep)
        except IndexError:
            error = "Couldn't retrieve keep"
            return None, error

        kept_users = restaurant_keep.get('user_id')
        if params.get('keep'):
            if params.get('myid') in kept_users:
                result = {'status': 'already there'}
                return result, error
            else:
                kept_users.append(params.get('myid'))
        else:
            if params.get('myid') in kept_users:
                kept_users.remove(params.get('myid'))
            else:
                result = {'status': 'already deleted'}
                return result, error

        logging.info(restaurant_keep)
        restaurant_keep['user_id'] = ', '.join(kept_users)
        toUpdate = {"user_id" : restaurant_keep.get('user_id')}
        logging.info(toUpdate)
        try:
            query_string = fiidup_sql.get_modify_query_string("restaurant_keep", toUpdate, "restaurant_id", id)
            cursor.execute(query_string)
            fiidup_sql.db.commit()
            return params, error
        except fiidup_sql.Error, e:
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
            cursor.close()
            handler.response.status = 403
            return None, error
    else:
        error = "ID not found"
        handler.response.status = 403
        return result, error

def get_keep(handler, id, params):
    # id represents dish_id
    data = None
    error = None
    cursor = fiidup_sql.db.cursor()
    if id:
        try:
            cond = {'restaurant_id': str(id)}
            query = fiidup_sql.get_retrieve_query_string(table='restaurant_keep', cond=cond)
            cursor.execute(query)
            datalist = cursor.fetchall()
            data = []
            keys = fiidup_sql.get_column_names('restaurant_keep')
            for x in datalist:
                x = dict(zip(keys, x))
                data.append(x)
            logging.info(data)
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            handler.response.status = 403
    else:
        error = "ID not found"
        handler.response.status = 403
    cursor.close()
    logging.info(data)
    return data, error
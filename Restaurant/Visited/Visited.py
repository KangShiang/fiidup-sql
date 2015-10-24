import sql
import logging
import MySQLdb

def put_visited(handler, id, params):
    # id represents dish_id
    # params should have the 'user_id' and 'tasted' fields
    data = None
    error = None
    change = None
    cursor = sql.db.cursor()
    if id:
        # extract only necessary info
        user_id = params.get('user_id')
        visited = params.get('visited')
        dict = {'restaurant_id': id, 'user_id': user_id}
        if user_id is None or visited is None:
            error = "Insufficient info to update restaurant_visited"
            handler.response.status = 403
        else:
            # encode user_id as ascii string
            user_id = user_id.encode('ascii')
            # query dish_tasted based on dish_id for user_id
            try:
                cond = {'restaurant_id': str(id)}
                query = sql.get_retrieve_query_string(table='restaurant_visited', cond=cond)
                cursor.execute(query)
                # expects only one result: ((dish_id, 'user_list'),)
                # user_list is a string
                user_list = cursor.fetchall()[0][1]
                user_list = user_list.strip('[]').split(', ')
                if user_list[0] == '':
                    user_list = list()
                # if tasted is True (user tasted this dish)
                # append user_id
                # increase tasted_count in dish table
                if visited == 'true' and user_id not in user_list:
                    logging.info("tasted")
                    user_list.append(user_id)
                    change = '+'
                # if tasted is False (user untasted this dish)
                # remove user_id
                # decrease tasted_count in dish table
                elif visited == 'false' and user_id in user_list:
                    logging.info("untasted")
                    user_list.remove(user_id)
                    change = '-'
                else:
                    # assuming tasted will only hold values: true or false, don't update table
                    logging.info("Not an error: May just be inconsistency in UI and database")
                    data = {'restaurant_id': id}
            except MySQLdb.Error, e:
                try:
                    logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                    error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                except IndexError:
                    logging.error("MySQL Error: %s" % str(e))
                    error = "MySQL Error: %s" % str(e)
                handler.response.status = 403

            if change is not None:
                # convert user_list to a string, remove "'" from individual elements
                user_list = str(user_list).replace("'", '')
                # modify entry in database: entry should exist upon restaurant creation
                logging.info(user_list)
                try:
                    query = sql.get_modify_query_string(table='restaurant_visited', params={'user_id': user_list},
                                                        primary_key='restaurant_id', id=id)
                    cursor.execute(query)
                    # change tasted_count in dish table
                    param = {'visited_count': 'visited_count %s 1' % change}
                    query = sql.get_modify_query_string(table='restaurant', params=param, primary_key='restaurant_id', id=id)
                    cursor.execute(query)
                    sql.db.commit()
                    data = {'restaurant_id': id}
                except MySQLdb.Error, e:
                    try:
                        logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                        error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                    except IndexError:
                        logging.error("MySQL Error: %s" % str(e))
                        error = "MySQL Error: %s" % str(e)
                    sql.db.rollback()
                    handler.response.status = 403
    else:
        error = "ID not found"
        handler.response.status = 403
    cursor.close()
    return data, error

def get_visited(handler, id, params):
    # id represents dish_id
    data = None
    error = None
    cursor = sql.db.cursor()
    if id:
        try:
            cond = {'restaurant_id': str(id)}
            query = sql.get_retrieve_query_string(table='restaurant_visited', cond=cond)
            cursor.execute(query)
            datalist = cursor.fetchall()
            data = []
            keys = sql.get_column_names('restaurant_visited')
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

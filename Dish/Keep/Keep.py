import sql
import logging
import MySQLdb

def put_keep(handler, id, params):
    # id represents dish_id
    # params should have the 'user_id' and 'keep' fields
    data = None
    error = None
    user_list = None
    cursor = sql.db.cursor()
    if id:
        # extract only necessary info
        user_id = params.get('user_id')
        keep = params.get('keep')
        dict = {'dish_id': id, 'user_id': user_id}
        if user_id is None or keep is None:
            error = "Insufficient info to update dish_keep"
            handler.response.status = 403
        else:
            # encode user_id as ascii string
            user_id = user_id.encode('ascii')
            # query dish_keep based on dish_id for user_id
            try:
                cond = {'dish_id': str(id)}
                query = sql.get_retrieve_query_string(table='dish_keep', cond=cond)
                cursor.execute(query)
                # expects only one result: ((dish_id, 'user_list'),)
                # user_list is a string
                user_list = cursor.fetchall()[0][1]
                user_list = user_list.strip('[]').split(', ')
                # if keep is True (user keeps this dish)
                # append user_id
                # increase keep_count in dish table
                if keep == 'True' and user_id not in user_list:
                    logging.info("keep")
                    user_list.append(user_id)
                # if keep is False (user unkeep this dish)
                # remove user_id
                # decrease keep_count in dish table
                elif keep == 'False' and user_id in user_list:
                    logging.info("unkeep")
                    user_list.remove(user_id)
                else:
                    # assuming keep will only hold values: true or false - ignore otherwise
                    logging.info("Not an error: May just be inconsistency in UI and database")
            except MySQLdb.Error, e:
                try:
                    logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                    error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                except IndexError:
                    logging.error("MySQL Error: %s" % str(e))
                    error = "MySQL Error: %s" % str(e)
                handler.response.status = 403

            # convert user_list to a string, remove "'" from individual elements
            user_list = str(user_list).replace("'", '')
            # modify entry in database: entry should exist upon dish creation
            logging.info(user_list)
            try:
                query = sql.get_modify_query_string(table='dish_keep', params={'user_id': user_list},
                                                    primary_key='dish_id', id=id)
                cursor.execute(query)
                sql.db.commit()
                data = {'dish_id': id}
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

def get_keep(handler, id, params):
    # id represents dish_id
    data = None
    error = None
    cursor = sql.db.cursor()
    if id:
        try:
            cond = {'dish_id': str(id)}
            query = sql.get_retrieve_query_string(table='dish_keep', cond=cond)
            cursor.execute(query)
            datalist = cursor.fetchall()
            data = []
            keys = sql.get_column_names('dish_keep')
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

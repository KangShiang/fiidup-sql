import sql
import logging
import MySQLdb

def put_like(handler, id, params):
    # id represents dish_id
    # params should have the 'user_id' and 'like' fields
    data = None
    error = None
    user_list = None
    cursor = sql.db.cursor()
    if id:
        # extract only necessary info
        user_id = params.get('user_id')
        like = params.get('like')
        dict = {'dish_id': id, 'user_id': user_id}
        if user_id is None or like is None:
            error = "Insufficient info to update dish_like"
            handler.response.status = 403
        else:
            # encode user_id as ascii string
            user_id = user_id.encode('ascii')
            # query dish_like based on dish_id for user_id
            try:
                cond = {'dish_id': str(id)}
                query = sql.get_retrieve_query_string(table='dish_like', cond=cond)
                cursor.execute(query)
                # expects only one result: ((dish_id, 'user_list'),)
                # user_list is a string
                user_list = cursor.fetchall()[0][1]
                user_list = user_list.strip('[]').split(', ')
                # if like is True (user likes this dish)
                # append user_id
                # increase like_count in dish table
                if like == 'True' and user_id not in user_list:
                    logging.info("like")
                    user_list.append(user_id)
                # if like is False (user unlike this dish)
                # remove user_id
                # decrease like_count in dish table
                elif like == 'False' and user_id in user_list:
                    logging.info("unlike")
                    user_list.remove(user_id)
                else:
                    # assuming like will only hold values: true or false - ignore otherwise
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
                query = sql.get_modify_query_string(table='dish_like', params={'user_id': user_list},
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

def get_like(handler, id, params):
    # id represents dish_id
    data = None
    error = None
    cursor = sql.db.cursor()
    if id:
        try:
            cond = {'dish_id': str(id)}
            query = sql.get_retrieve_query_string(table='dish_like', cond=cond)
            cursor.execute(query)
            datalist = cursor.fetchall()
            data = []
            keys = sql.get_column_names('dish_like')
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

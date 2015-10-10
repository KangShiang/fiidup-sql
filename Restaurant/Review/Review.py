import MySQLdb
import sql
import logging

def delete_review(handler, id, params):
    # id represents comment_id
    data = None
    error = None
    cursor = sql.db.cursor()
    if id:
        try:
            query = sql.get_delete_query_string('review', 'review_id', id)
            cursor.execute(query)
            # decrement comment_count in dish table
            param = {'review_count': 'review_count - 1'}
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
        error = "Key not found"
        handler.response.status = 403
    cursor.close()
    return data, error

def get_review(handler, id, params):
    # id represents dish_id
    data = None
    error = None
    cursor = sql.db.cursor()
    if id:
        try:
            cond = {'restaurant_id': str(id)}
            query = sql.get_retrieve_query_string(table='review', cond=cond)
            cursor.execute(query)
            try:
                datalist = cursor.fetchall()
                data = []
                keys = sql.get_column_names('review')
                for x in datalist:
                    x = dict(zip(keys, x))
                    data.append(x)
            except IndexError:
                data = []
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

'''
Returns the review_id
'''
def post_comment(handler, id, params):
    # id represents restaurant_id
    # input params should have the comment string and user_id of the user who posts the comment
    data = None
    error = None
    cursor = sql.db.cursor()
    if id:
        # extract only necessary info
        user_id = params.get('user_id')
        review = params.get('review')
        dict = {'restaurant_id': id, 'user_id': user_id, 'review': review}
        if (user_id is None) or (comment is None):
            error = "Insufficient info to post comment"
            handler.response.status = 403
        else:
            try:
                query = sql.get_insert_query_string('review', dict)
                cursor.execute(query)
                # increment comment_count in dish table
                param = {'review_count': 'review_count + 1'}
                query = sql.get_modify_query_string(table='restaurant', params=param, primary_key='restaurant_id', id=id)
                cursor.execute(query)
                sql.db.commit()
                data = {'review_id': sql.get_last_inserted_pkey(cursor)}
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

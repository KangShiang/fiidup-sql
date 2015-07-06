import webapp2
import MySQLdb
import sql
import utils
import logging

def delete_comment(handler, id, params):
    # id represents dish_id
    data = None
    error = None
    cursor = sql.db.cursor()
    if id:
        # extract only necessary info
        comment_id = params.get('comment_id')
        if comment_id is None:
            error = "Insufficient info to delete comment"
            handler.response.status = 403
        else:
            try:
                query = sql.get_delete_query_string('comment', 'comment_id', comment_id)
                cursor.execute(query)
                sql.db.commit()
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

def get_comment(handler, id, params):
    # id represents dish_id
    data = None
    error = None
    cursor = sql.db.cursor()
    if id:
        try:
            cond = {'dish_id': str(id)}
            query = sql.get_retrieve_query_string(table='comment', cond=cond)
            cursor.execute(query)
            try:
                datalist = cursor.fetchall()
                data = []
                keys = sql.get_column_names('comment')
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
Returns the comment_id
'''
def post_comment(handler, id, params):
    # id represents dish_id
    # input params should have the comment string and user_id of the user who posts the comment
    data = None
    error = None
    cursor = sql.db.cursor()
    if id:
        # extract only necessary info
        user_id = params.get('user_id')
        comment = params.get('comment')
        dict = {'dish_id': id, 'user_id': user_id, 'comment': comment}
        if (user_id is None) or (comment is None):
            error = "Insufficient info to post comment"
            handler.response.status = 403
        else:
            try:
                query = sql.get_insert_query_string('comment', dict)
                cursor.execute(query)
                sql.db.commit()
                data = {'comment_id': sql.get_last_inserted_pkey(cursor)}
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

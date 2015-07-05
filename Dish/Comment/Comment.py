import webapp2
import MySQLdb
import sql
import utils
import logging

def put_comment(handler, id, params):
    if id:
        handler.response.out.write("Put to comment " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.status = 403

def get_comment(handler, id, params):
    # id represents dish_id
    # params is assumed to contain user_id
    error = None
    cursor = sql.db.cursor()
    if id:
        try:
            cond = {'dish_id': str(id)}
            query = sql.get_retrieve_query_string(table='comment', cond=cond)
            cursor.execute(query)
            data = cursor.fetchall()[0]
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            handler.response.status = 403
            data = None
        cursor.execute("DESCRIBE comment")
        keys = [x[0] for x in cursor.fetchall()]
        cursor.close()
        data = dict(zip(keys, data))
        k = utils.generate_json(handler.request, params.get('user_id'), 'GET', data, error)
        handler.response.out.write(k)
        return data, error
    else:
        error = "ID not found"
        handler.response.status = 403
        return None, error

def post_comment(handler, id, params):
    # id represents dish_id
    # input params should have the comment string and user_id of the user who posts the comment
    if id:
        table = 'comment'
        # extract only necessary info
        user_id = params.get('user_id')
        comment = params.get('comment')
        dict = {'dish_id': id, 'user_id': user_id, 'comment': comment}
        if (user_id is None) or (comment is None):
            handler.response.status = 403
        else:
            query = sql.get_insert_query_string(table, dict)
            print params
    else:
        handler.response.status = 403

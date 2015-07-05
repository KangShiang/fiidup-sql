import webapp2
import sql

def put_comment(handler, id, params):
    if id:
        handler.response.out.write("Put to comment " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.status = 403

def get_comment(handler, id, params):
    # id represents dish_id
    # params is assumed to be empty
    if id:
        table = 'comment'
        cond = {'dish_id': str(id)}
        query = sql.get_retrieve_query_string(table, [], cond)
        cursor = sql.db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

    else:
        handler.response.status = 403

def post_comment(handler, id, params):
    if id:
        handler.response.out.write("Post to comment " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.status = 403
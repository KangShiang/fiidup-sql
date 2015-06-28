import webapp2

def put_comment(handler, id, params):
    if id:
        handler.response.out.write("Put to comment " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Put to comment")

def get_comment(handler, id, params):
    if id:
        handler.response.out.write("Get to comment " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to comment")

def post_comment(handler, id, params):
    if id:
        handler.response.out.write("Post to comment " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to comment")
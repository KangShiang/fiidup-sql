import webapp2

def put_like(handler, id, params):
    if id:
        handler.response.out.write("Put to like " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Put to like")

def get_like(handler, id, params):
    if id:
        handler.response.out.write("Get to like " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to like")

def post_like(handler, id, params):
    if id:
        handler.response.out.write("Post to like " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to like")
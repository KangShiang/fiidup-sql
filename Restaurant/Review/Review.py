import webapp2

def put_review(handler, id, params):
    if id:
        handler.response.out.write("Put to comment " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Put to comment")

def Review(handler, id, params):
    if id:
        handler.response.out.write("Get to comment " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to comment")

def post_review(handler, id, params):
    if id:
        handler.response.out.write("Post to comment " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to comment")
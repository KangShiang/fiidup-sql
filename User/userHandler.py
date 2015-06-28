import webapp2

def put_user(handler, id, params):
    if id:
        handler.response.out.write("Put to user " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Put to user" + " and Param =" + str(params))

def get_user(handler, id, params):
    if id:
        handler.response.out.write("Get to user " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to user" + " and Param =" + str(params))

def post_user(handler, id, params):
    if id:
        handler.response.out.write("Post to user " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to user" + " and Param =" + str(params))
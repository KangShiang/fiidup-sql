import webapp2

def put_keep(handler, id, params):
    if id:
        handler.response.out.write("Put to keep " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Put to keep" + " and Param =" + str(params))

def get_keep(handler, id, params):
    if id:
        handler.response.out.write("Get to keep " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to keep" + " and Param =" + str(params))

def post_keep(handler, id, params):
    if id:
        handler.response.out.write("Post to keep " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to keep" + " and Param =" + str(params))
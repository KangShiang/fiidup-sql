import webapp2

def put_keep(handler, id, params):
    if id:
        handler.response.out.write("Put to keep " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Put to keep")

def get_keep(handler, id, params):
    if id:
        handler.response.out.write("Get to keep " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to keep")

def post_keep(handler, id, params):
    if id:
        handler.response.out.write("Post to keep " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to keep")
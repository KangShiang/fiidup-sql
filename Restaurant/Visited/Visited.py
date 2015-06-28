import webapp2

def put_visited(handler, id, params):
    if id:
        handler.response.out.write("Put to visited " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Put to visited" + " and Param =" + str(params))

def get_visited(handler, id, params):
    if id:
        handler.response.out.write("Get to visited " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to visited" + " and Param =" + str(params))

def post_visited(handler, id, params):
    if id:
        handler.response.out.write("Post to visited " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to visited" + " and Param =" + str(params))
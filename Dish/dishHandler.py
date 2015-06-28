import webapp2

def put_dish(handler, id, params):
    if id:
        handler.response.out.write("Put to dish " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Put to dish" + " and Param =" + str(params))

def get_dish(handler, id, params):
    if id:
        handler.response.out.write("Get to dish " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to dish" + " and Param =" + str(params))

def post_dish(handler, id, params):
    if id:
        handler.response.out.write("Post to dish " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to dish" + " and Param =" + str(params))
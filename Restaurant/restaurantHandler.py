import webapp2

def put_restaurant(handler, id, params):
    if id:
        handler.response.out.write("Put to restaurant " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Put to restaurant" + " and Param =" + str(params))

def get_restaurant(handler, id, params):
    if id:
        handler.response.out.write("Get to restaurant " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to restaurant" + " and Param =" + str(params))

def post_restaurant(handler, id, params):
    if id:
        handler.response.out.write("Post to restaurant " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to restaurant" + " and Param =" + str(params))
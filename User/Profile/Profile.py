import webapp2

def put_profile(handler, id, params):
    if id:
        handler.response.out.write("Put to profile " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Put to profile" + " and Param =" + str(params))

def get_profile(handler, id, params):
    if id:
        handler.response.out.write("Get to profile " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to profile" + " and Param =" + str(params))

def post_profile(handler, id, params):
    if id:
        handler.response.out.write("Post to profile " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to profile" + " and Param =" + str(params))

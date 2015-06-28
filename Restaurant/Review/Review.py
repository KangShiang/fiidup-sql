import webapp2

def put_review(handler, id, params):
    if id:
        handler.response.out.write("Put to review " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Put to review" + "when id = " + id + " and Param =" + str(params))

def get_review(handler, id, params):
    if id:
        handler.response.out.write("Get to review " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to review" + "when id = " + id + " and Param =" + str(params))

def post_review(handler, id, params):
    if id:
        handler.response.out.write("Post to review " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to review" + "when id = " + id + " and Param =" + str(params))
import webapp2

def delete_session(handler, id, params):
    if id:
        handler.response.out.write("Delete session " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Delete session" + " and Param =" + str(params))

def get_session(handler, id, params):
    if id:
        handler.response.out.write("Get to session " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Get to session" + " and Param =" + str(params))

def post_session(handler, id, params):
    if id:
        handler.response.out.write("Post to session " + "when id = " + id + " and Param =" + str(params))
    else:
        handler.response.out.write("Post to session" + " and Param =" + str(params))
import webapp2

def put_keep(handler, id):
    if id:
        handler.response.out.write("Put to keep " + "when id = " + id )
    else:
        handler.response.out.write("Put to keep")

def get_keep(handler, id):
    if id:
        handler.response.out.write("Get to keep " + "when id = " + id )
    else:
        handler.response.out.write("Get to keep")

def post_keep(handler, id):
    if id:
        handler.response.out.write("Post to keep " + "when id = " + id )
    else:
        handler.response.out.write("Post to keep")
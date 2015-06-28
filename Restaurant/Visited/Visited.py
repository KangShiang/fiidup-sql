import webapp2

def put_visited(handler, id):
    if id:
        handler.response.out.write("Put to visited " + "when id = " + id )
    else:
        handler.response.out.write("Put to visited")

def get_visited(handler, id):
    if id:
        handler.response.out.write("Get to visited " + "when id = " + id )
    else:
        handler.response.out.write("Get to visited")

def post_visited(handler, id):
    if id:
        handler.response.out.write("Post to visited " + "when id = " + id )
    else:
        handler.response.out.write("Post to visited")
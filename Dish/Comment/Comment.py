import webapp2

def put_comment(handler, id):
    if id:
        handler.response.out.write("Put to comment " + "when id = " + id )
    else:
        handler.response.out.write("Put to comment")

def get_comment(handler, id):
    if id:
        handler.response.out.write("Get to comment " + "when id = " + id )
    else:
        handler.response.out.write("Get to comment")

def post_comment(handler, id):
    if id:
        handler.response.out.write("Post to comment " + "when id = " + id )
    else:
        handler.response.out.write("Post to comment")
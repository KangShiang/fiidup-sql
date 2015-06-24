import webapp2

def put_tasted(handler, id):
    if id:
        handler.response.out.write("Put to tasted " + "when id = " + id )
    else:
        handler.response.out.write("Put to tasted")

def get_tasted(handler, id):
    if id:
        handler.response.out.write("Get to tasted " + "when id = " + id )
    else:
        handler.response.out.write("Get to tasted")

def post_tasted(handler, id):
    if id:
        handler.response.out.write("Post to tasted " + "when id = " + id )
    else:
        handler.response.out.write("Post to tasted")
import webapp2

def put_comment(handler):
    handler.response.out.write("Put to comment")

def get_comment(handler):
    handler.response.out.write("Get to comment")

def post_comment(handler):
    handler.response.out.write("Post to comment")
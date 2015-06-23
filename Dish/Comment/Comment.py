import webapp2


def post_comment(handler):
    handler.response.out.write("Post to comment")
    return handler
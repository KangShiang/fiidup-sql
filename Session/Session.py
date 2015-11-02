import webapp2
import utils
import urlparse
import sessionHandler

class Session(webapp2.RequestHandler):
    def get(self):
        url_string = str(self.request.url)
        url_obj = urlparse.urlparse(url_string)
        subdirs = str(url_obj.path).split('/')
        num_layers = len(subdirs)
        if num_layers == 2:
            sessionHandler.get_session(self)
        else:
            self.response.status = 405

    def post(self):
        err, req_params = utils.validate_data(self.request)
        if err:
            self.response.out.write(err.message())
            return

        url_string = str(self.request.url)
        url_obj = urlparse.urlparse(url_string)
        subdirs = str(url_obj.path).split('/')
        num_layers = len(subdirs)
        if num_layers == 2:
            sessionHandler.post_session(self, req_params)
        else:
            self.response.status = 405

    def delete(self):
        url_string = str(self.request.url)
        url_obj = urlparse.urlparse(url_string)
        subdirs = str(url_obj.path).split('/')
        num_layers = len(subdirs)
        if num_layers == 2:
            sessionHandler.delete_session(self)
        else:
            self.response.status = 405

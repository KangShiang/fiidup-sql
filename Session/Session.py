import webapp2
import utils
import urlparse
import sessionHandler

class Session(webapp2.RequestHandler):
    def get(self):
        err, req_params = utils.validate_data(self.request)
        if err:
            self.response.out.write(err.message())
            return

        url_string = str(self.request.url)
        url_obj = urlparse.urlparse(url_string)
        # str.split returns a list of strings. Google search python str.split for more detail.
        subdirs = str(url_obj.path).split('/')
        # Last element in the url
        last_dir_string = str(subdirs[len(subdirs)-1])
        num_layers = len(subdirs)
        if num_layers == 2:
            sessionHandler.get_session(self, None, req_params)
        else:
            self.response.status = 405

    def post(self):
        err, req_params = utils.validate_data(self.request)
        if err:
            self.response.out.write(err.message())
            return

        url_string = str(self.request.url)
        url_obj = urlparse.urlparse(url_string)
        # str.split returns a list of strings. Google search python str.split for more detail.
        subdirs = str(url_obj.path).split('/')
        # Last element in the url
        last_dir_string = str(subdirs[len(subdirs)-1])
        num_layers = len(subdirs)
        if num_layers == 2:
            sessionHandler.post_session(self, None, req_params)
        else:
            self.response.status = 405

    def delete(self):
        err, req_params = utils.validate_data(self.request)
        if err:
            self.response.out.write(err.message())
            return

        url_string = str(self.request.url)
        url_obj = urlparse.urlparse(url_string)
        # str.split returns a list of strings. Google search python str.split for more detail.
        subdirs = str(url_obj.path).split('/')
        # Last element in the url
        last_dir_string = str(subdirs[len(subdirs)-1])
        num_layers = len(subdirs)
        if num_layers == 2:
            sessionHandler.delete_session(self, None, req_params)
        else:
            self.response.status = 405

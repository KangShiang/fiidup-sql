import webapp2
import utils
import urlparse
import userHandler

put_sub_routes = {"PUT_profile": "put_profile"}

get_sub_routes = {"GET_profile": "get_profile"}

post_sub_routes = {"POST_profile": "post_profile"}

class User(webapp2.RequestHandler):
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
            userHandler.get_user(self, None, req_params)
        elif num_layers == 3:
            try:
                # Handle the case when the url is /user/:id
                int(last_dir_string)
                userHandler.get_user(self, last_dir_string, req_params)
            except ValueError:
                try:
                    subdir_string = str(subdirs[2])
                    handling_function = get_sub_routes["GET_" + subdir_string]
                    getattr(globals()[subdir_string + "Handler"], handling_function)(self, None, req_params)
                except KeyError:
                    self.response.status = 405
        elif num_layers == 4:
            try:
                # Handle the case when the url is /user/.../:id
                int(last_dir_string)
                subdir_string = str(subdirs[2])
                handling_function = get_sub_routes["GET_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self, last_dir_string, req_params)
                # Return info of a specific user
            except KeyError:
                self.response.status = 405
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
        # Last element in the url
        last_dir_string = str(subdirs[len(subdirs)-1])
        num_layers = len(subdirs)

        # Only Handle the case of /user
        if num_layers == 2 and last_dir_string == "user":
            userHandler.post_user(self, None, req_params)
        elif num_layers == 3:
            try:
                # Handling the case of /user/...
                subdir_string = str(subdirs[2])
                handling_function = post_sub_routes["POST_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self , None, req_params)
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405

    def put(self):
        err, req_params = utils.validate_data(self.request)
        if err:
            self.response.out.write(err.message())
            return

        url_string = str(self.request.url)
        url_obj = urlparse.urlparse(url_string)
        subdirs = str(url_obj.path).split('/')
        # Last element in the url
        last_dir_string = str(subdirs[len(subdirs)-1])
        num_layers = len(subdirs)

        # Only Handle the case of /user
        if num_layers == 2 and last_dir_string == "user":
            userHandler.put_user(self, None, req_params)
        elif num_layers == 3:
            try:
                # Handling the case of /user/...
                subdir_string = str(subdirs[2])
                handling_function = post_sub_routes["POST_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self , None, req_params)
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405

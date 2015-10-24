import webapp2
import utils
import urlparse
import userHandler
from Follower import Follower as followerHandler
from Following import Following as followingHandler

put_sub_routes = {"PUT_profile": "put_profile",
                  "PUT_following": "put_following"}

get_sub_routes = {"GET_profile": "get_profile",
                  "GET_follower": "get_follower",
                  "GET_following": "get_following"}

post_sub_routes = {"POST_profile": "post_profile"}

delete_sub_routes = {"DELETE_following": "delete_following"}

class User(webapp2.RequestHandler):
    def get(self):
        data = None
        error = None
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
                    data, error = getattr(globals()[subdir_string + "Handler"], handling_function)(self, None, req_params)
                except KeyError:
                    self.response.status = 405
        elif num_layers == 4:
            try:
                # Handle the case when the url is /user/.../:id
                int(last_dir_string)
                subdir_string = str(subdirs[2])
                handling_function = get_sub_routes["GET_" + subdir_string]
                data, error = getattr(globals()[subdir_string + "Handler"], handling_function)(self, last_dir_string, req_params)
                # Return info of a specific user
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405
        self.response.out.write(utils.generate_json(self.request, 123, "GET", data, error))

    def post(self):
        data = None
        error = None
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
                data, error = getattr(globals()[subdir_string + "Handler"], handling_function)(self, None, req_params)
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405
        self.response.out.write(utils.generate_json(self.request, 123, "POST", data, error))

    def put(self):
        data = None
        error = None
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
                handling_function = put_sub_routes["PUT_" + subdir_string]
                data, error = getattr(globals()[subdir_string + "Handler"], handling_function)(self, None, req_params)
            except KeyError:
                self.response.status = 405
        elif num_layers == 4:
            try:
                # Handle the case when the url is /user/.../:id
                int(last_dir_string)
                subdir_string = str(subdirs[2])
                handling_function = put_sub_routes["PUT_" + subdir_string]
                data, error = getattr(globals()[subdir_string + "Handler"], handling_function)(self, last_dir_string, req_params)
                # Return info of a specific user
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405
        self.response.out.write(utils.generate_json(self.request, 123, "PUT", data, error))

    def delete(self):
        data = None
        error = None
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

        try:
            int(last_dir_string)
        except ValueError:
            error = "ID not found"
            self.response.status = 403

        if num_layers == 3:
            data, error = userHandler.delete_user(self, last_dir_string, req_params)
        elif num_layers == 4:
            try:
                subdir_string = str(subdirs[2])
                handling_function = delete_sub_routes["DELETE_" + subdir_string]
                data, error = getattr(globals()[subdir_string + "Handler"], handling_function)(self, last_dir_string, req_params)
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405
        self.response.out.write(utils.generate_json(self.request, 123, "DELETE", data, error))

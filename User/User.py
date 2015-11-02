import webapp2
import utils
import urlparse
import userHandler
from Follower import Follower as followerHandler
from Following import Following as followingHandler

put_sub_routes = {"PUT_following": "put_following"}

get_sub_routes = {"GET_follower": "get_follower",
                  "GET_following": "get_following"}

delete_sub_routes = {"DELETE_following": "delete_following"}

class User(webapp2.RequestHandler):
    def get(self):
        authenticated, this_user = utils.process_cookie(self.request)
        if not authenticated:
            self.response.status = 401
            return

        url_obj = urlparse.urlparse(str(self.request.url))
        subdirs = str(url_obj.path).split('/')
        num_layers = len(subdirs)
        last_dir_string = str(subdirs[len(subdirs)-1])

        if num_layers == 2:
            userHandler.get_user(self, this_user, this_user)
        elif num_layers == 3:
            try:
                target_user = int(last_dir_string)
                userHandler.get_user(self, this_user, target_user)
            except ValueError:
                self.response.status = 405
        elif num_layers == 4:
            try:
                target_user = int(subdirs[2])
                subdir_string = str(last_dir_string)
                handling_function = get_sub_routes["GET_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self, this_user, target_user)
            except ValueError:
                self.response.status = 405
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405

    def post(self):
        authenticated, this_user = utils.process_cookie(self.request)
        if authenticated:
            # a user should not be authenticated to sign up
            error = 'You are already a Fiider!'
            self.response.out.write(utils.generate_json(self.request, this_user, "POST", None, error))
            self.response.status = 403
            return

        err, req_params = utils.validate_data(self.request)
        if err:
            self.response.out.write(utils.generate_json(self.request, this_user, "POST", None, err.message()))
            self.response.status = 403
            return

        url_obj = urlparse.urlparse(str(self.request.url))
        subdirs = str(url_obj.path).split('/')
        num_layers = len(subdirs)

        # Only Handle the case of /user
        if num_layers == 2:
            userHandler.post_user(self, this_user, req_params)
        else:
            self.response.status = 405

    def put(self):
        authenticated, this_user = utils.process_cookie(self.request)
        if not authenticated:
            self.response.status = 401
            return

        err, req_params = utils.validate_data(self.request)
        if err:
            self.response.out.write(utils.generate_json(self.request, this_user, "PUT", None, err.message()))
            self.response.status = 403
            return

        url_obj = urlparse.urlparse(str(self.request.url))
        subdirs = str(url_obj.path).split('/')
        num_layers = len(subdirs)
        last_dir_string = str(subdirs[len(subdirs)-1])

        if num_layers == 2:
            userHandler.put_user(self, this_user, req_params)
        elif num_layers == 4:
            try:
                url_user = int(subdirs[2])
                if this_user == url_user:
                    subdir_string = str(last_dir_string)
                    handling_function = put_sub_routes["PUT_" + subdir_string]
                    getattr(globals()[subdir_string + "Handler"], handling_function)(self, this_user, req_params)
                else:
                    self.response.status = 401
            except ValueError:
                self.response.status = 405
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405

    def delete(self):
        authenticated, this_user = utils.process_cookie(self.request)
        if not authenticated:
            self.response.status = 401
            return

        url_obj = urlparse.urlparse(str(self.request.url))
        subdirs = str(url_obj.path).split('/')
        num_layers = len(subdirs)
        last_dir_string = str(subdirs[len(subdirs)-1])

        if num_layers == 2:
            userHandler.delete_user(self, this_user)
        elif num_layers == 5:
            try:
                if this_user == int(subdirs[2]):
                    subdir_string = str(subdirs[3])
                    target_user = int(last_dir_string)
                    handling_function = delete_sub_routes["DELETE_" + subdir_string]
                    getattr(globals()[subdir_string + "Handler"], handling_function)(self, this_user, target_user)
                else:
                    self.response.status = 401
            except ValueError:
                self.response.status = 405
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405

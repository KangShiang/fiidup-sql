import webapp2
import utils
import urlparse
import dishHandler
from Comment import Comment as commentHandler
from Like import Like as likeHandler
from Tasted import Tasted as tastedHandler
from Keep import Keep as keepHandler

get_sub_routes = {"GET_comment": "get_comment",
                  "GET_like": "get_like",
                  "GET_tasted": "get_tasted",
                  "GET_keep": "get_keep"}

post_sub_routes = {"POST_comment": "post_comment",
                   "POST_like": "post_like",
                   "POST_tasted": "post_tasted",
                   "POST_keep": "post_keep"}

delete_sub_routes = {"DELETE_comment": "delete_comment",
                     "DELETE_like": "delete_like",
                     "DELETE_tasted": "delete_tasted",
                     "DELETE_keep": "delete_keep"}

class Dish(webapp2.RequestHandler):
    POST_BLACKLIST = ['dish_id', 'user_id', 'posted_time', 'like_count', 'comment_count',
                      'tasted_count', 'keep_count', 'comment_id']
    PUT_BLACKLIST = ['dish_id', 'user_id', 'url', 'posted_time', 'like_count', 'comment_count',
                     'tasted_count', 'keep_count']

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
            dishHandler.get_dish(self, this_user, None)
        elif num_layers == 3:
            try:
                target_dish = int(last_dir_string)
                dishHandler.get_dish(self, this_user, target_dish)
            except ValueError:
                self.response.status = 405
        elif num_layers == 4:
            try:
                target_dish = int(subdirs[2])
                subdir_string = str(last_dir_string)
                handling_function = get_sub_routes["GET_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self, this_user, target_dish)
            except ValueError:
                self.response.status = 405
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405

    def post(self):
        authenticated, this_user = utils.process_cookie(self.request)
        if not authenticated:
            self.response.status = 401
            return

        err, req_params = utils.validate_data(self.request)
        if err:
            self.response.out.write(utils.generate_json(self.request, this_user, "POST", None, err.message()))
            self.response.status = 403
            return

        if utils.fail_blacklist(self.POST_BLACKLIST, req_params):
            error = 'Invalid data in body'
            self.response.out.write(utils.generate_json(self.request, this_user, "POST", None, error))
            self.response.status = 403
            return

        url_obj = urlparse.urlparse(str(self.request.url))
        subdirs = str(url_obj.path).split('/')
        num_layers = len(subdirs)
        last_dir_string = str(subdirs[len(subdirs)-1])

        if num_layers == 2:
            dishHandler.post_dish(self, this_user, req_params)
        elif num_layers == 4:
            try:
                target_dish = int(subdirs[2])
                subdir_string = str(last_dir_string)
                handling_function = post_sub_routes["POST_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self, this_user, target_dish,
                                                                                 req_params)
            except ValueError:
                self.response.status = 405
            except KeyError:
                self.response.status = 405
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

        if utils.fail_blacklist(self.PUT_BLACKLIST, req_params):
            error = 'Invalid data in body'
            self.response.out.write(utils.generate_json(self.request, this_user, "PUT", None, error))
            self.response.status = 403
            return

        url_obj = urlparse.urlparse(str(self.request.url))
        subdirs = str(url_obj.path).split('/')
        num_layers = len(subdirs)
        last_dir_string = str(subdirs[len(subdirs)-1])

        if num_layers == 3:
            try:
                target_dish = int(last_dir_string)
                dishHandler.put_dish(self, this_user, target_dish, req_params)
            except ValueError:
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

        if num_layers == 3:
            try:
                target_dish = int(last_dir_string)
                dishHandler.delete_dish(self, this_user, target_dish)
            except ValueError:
                self.response.status = 405
        elif num_layers == 4:
            try:
                target_dish = int(subdirs[2])
                subdir_string = str(last_dir_string)
                handling_function = delete_sub_routes["DELETE_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self, this_user, target_dish)
            except ValueError:
                self.response.status = 405
            except KeyError:
                self.response.status = 405
        elif num_layers == 5 and subdirs[3] == 'comment':
            try:
                target_dish = int(subdirs[2])
                target_comment = int(last_dir_string)
                commentHandler.delete_comment(self, this_user, target_dish, target_comment)
            except ValueError:
                self.response.status = 405
        else:
            self.response.status = 405

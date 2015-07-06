import webapp2
import utils
import urlparse
import dishHandler
import logging
import sql as fiidup_sql
from Comment import Comment as commentHandler
from Like import Like as likeHandler
from Tasted import Tasted as tastedHandler
from Keep import Keep as keepHandler

put_sub_routes = {"PUT_comment": "put_comment",
                  "PUT_like": "put_like",
                  "PUT_tasted": "put_tasted",
                  "PUT_keep": "put_keep"}

get_sub_routes = {"GET_comment": "get_comment",
                  "GET_like": "get_like",
                  "GET_tasted": "get_tasted",
                  "GET_keep": "get_keep"}

post_sub_routes = {"POST_comment": "post_comment",
                   "POST_like": "post_like",
                   "POST_tasted": "post_tasted",
                   "POST_keep": "post_keep"}


class Dish(webapp2.RequestHandler):
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
            data, error = dishHandler.get_dish(self, None, req_params)
        elif num_layers == 3:
            try:
                # Handle the case when the url is /dish/<id>
                int(last_dir_string)
                data, error = dishHandler.get_dish(self, last_dir_string, req_params)
                logging.info(data)
                logging.info(error)

            except ValueError:
                try:
                    subdir_string = str(subdirs[2])
                    handling_function = get_sub_routes["GET_" + subdir_string]
                    getattr(globals()[subdir_string + "Handler"], handling_function)(self, None, req_params)

                except KeyError:
                    self.response.status = 405

        elif num_layers == 4:
            try:
                # Handle the case when the url is /dish/<info>:id
                int(last_dir_string)
                subdir_string = str(subdirs[2])
                handling_function = get_sub_routes["GET_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self, last_dir_string, req_params)
                # Return info of a specific dish
            except KeyError:
                self.response.status = 405

        else:
            self.response.status = 405
        self.response.out.write(utils.generate_json(self.request, 123, "GET", data, error))


    def post(self):
        '''
        authenticated, user = utils.process_cookie(self.request, self.response)
        if not authenticated:
            return
'''
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

        # Only Handle the case of /dish
        if num_layers == 2 and last_dir_string == "dish":
            dishHandler.post_dish(self, None, req_params)
            return
        elif num_layers == 3:
            try:
                subdir_string = str(subdirs[2])
                handling_function = post_sub_routes["POST_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self, None, req_params)
                return
            except KeyError:
                self.response.status = 405
                return
        elif num_layers == 4:
            try:
                subdir_string = str(subdirs[2])
                handling_function = post_sub_routes["POST_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self, last_dir_string, req_params)
                return
            except KeyError:
                self.response.status = 405
                return
        else:
            self.response.status = 405

    def put(self):
        data = None
        error = None
        #authenticated, user = utils.process_cookie(self.request, self.response)
        # if not authenticated:
        #     return
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

        try:
            int(last_dir_string)
        except ValueError:
            error = "ID not found"
            self.response.out.write(utils.generate_json(self.request, 123, "PUT", None, error))
            self.response.status = 403
            return

        if num_layers == 3:
            data, error = dishHandler.put_dish(self, last_dir_string, req_params)
        elif num_layers == 4:
            try:
                subdir_string = str(subdirs[2])
                handling_function = put_sub_routes["PUT_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self, last_dir_string, req_params)
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405
        self.response.out.write(utils.generate_json(self.request, 123, "GET", data, error))
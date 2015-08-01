import webapp2
import logging
import utils
import MySQLdb
import sql as fiidup_sql
import urlparse
import json
import restaurantHandler

from Like import Like as likeHandler
from Visited import Visited as visitedHandler
from Review import Review as reviewHandler
from Keep import Keep as keepHandler

put_sub_routes = {"PUT_like": "put_like",
                  "PUT_visited": "put_visited",
                  "PUT_review": "put_review",
                  "PUT_keep": "put_keep"}

get_sub_routes = {"GET_like": "get_like",
                  "GET_visited": "get_visited",
                  "GET_review": "get_review",
                  "GET_keep": "get_keep"}

post_sub_routes = {"POST_like": "post_like",
                   "POST_visited": "post_visited",
                   "POST_review": "post_review",
                   "POST_keep": "post_keep"}

class Restaurant(webapp2.RequestHandler):
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
            data, error = restaurantHandler.get_restaurant(self, None, req_params)
        elif num_layers == 3:
            try:
                # Handle the case when the url is /dish/<id>
                int(last_dir_string)
                data, error = restaurantHandler.get_restaurant(self, last_dir_string, req_params)
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

        # Only Handle the case of /dish
        if num_layers == 2 and last_dir_string == "restaurant":
            data, error = restaurantHandler.post_restaurant(self, None, req_params)
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
        self.response.out.write(utils.generate_json(self.request, 123, "GET", data, error))

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
            data, error = restaurantHandler.put_restaurant(self, last_dir_string, req_params)
        elif num_layers == 4:
            try:
                subdir_string = str(subdirs[2])
                handling_function = put_sub_routes["PUT_" + subdir_string]
                logging.info(handling_function)
                getattr(globals()[subdir_string + "Handler"], handling_function)(self, last_dir_string, req_params)
            except KeyError:
                self.response.status = 405
        else:
            self.response.status = 405
        self.response.out.write(utils.generate_json(self.request, 123, "GET", data, error))


    def delete(self):
        data = None
        error = None
        #authenticated, user = utils.process_cookie(self.request, self.response)
        # if not authenticated:
        #     return

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
            data, error = restaurantHandler.delete_restaurant(self, last_dir_string)
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

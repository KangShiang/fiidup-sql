import webapp2
import logging
import utils
import MySQLdb
import sql as fiidup_sql
import urlparse
import json
from Comment import Comment as commentHandler
from Like import Like as LikeHandler
from Tasted import Tasted as TastedHandler
from Keep import Keep as KeepHandler

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
            self.response.out.write("Retrieve Data")
            return
        elif num_layers == 3:
            try:
                # Handle the case when the url is /dish/:id
                int(last_dir_string)
                # Return info of a specific dish
            except ValueError:
                try:
                    subdir_string = str(subdirs[2])
                    handling_function = get_sub_routes["GET_" + subdir_string]
                    getattr(globals()[subdir_string + "Handler"], handling_function)(self)
                    return
                except KeyError:
                    self.response.out.write("Invalid URL")
                    return
        self.response.out.write("Invalid URL")

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

        # Only Handle the case of /dish
        if num_layers == 2 and last_dir_string == "dish":
            cursor = fiidup_sql.db.cursor()
            try:
                query = fiidup_sql.get_insert_query_string("dish", req_params)
                cursor.execute(query)
                fiidup_sql.db.commit()
            except MySQLdb.Error, e:
                try:
                    logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                except IndexError:
                    logging.error("MySQL Error: %s" % str(e))

            self.response.out.write(json.dumps(req_params))
            return
        elif num_layers == 3:
            try:
                subdir_string = str(subdirs[2])
                handling_function = post_sub_routes["POST_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self)
                return
            except KeyError:
                self.response.out.write("Invalid URL")
                return
        else:
            self.response.out.write("Invalid URL")

    def put(self):
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
            self.response.out.write("Invalid URL")
            return

        if num_layers == 3:
            self.response.out.write("Modify Data")
            return
        elif num_layers == 4:
            try:
                subdir_string = str(subdirs[2])
                handling_function = put_sub_routes["PUT_" + subdir_string]
                getattr(globals()[subdir_string + "Handler"], handling_function)(self)
                return
            except KeyError:
                self.response.out.write("Invalid URL")
                return
        self.response.out.write("Invalid URL")
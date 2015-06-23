import webapp2
import logging
import utils
import MySQLdb
import sql as fiidup_sql
import urlparse
import json
from Comment import Comment as CommentHandler

post_sub_routes = {"comment": "post_comment",
                   "like": "post_like",
                   "tasted": "post_tasted",
                   "keep": "post_keep"}


class Dish(webapp2.RequestHandler):
    def get(self):
        err, req_params = utils.validate_data(self.request)
        if err:
            self.response.out.write(err.message())
            return
        self.response.out.write(req_params)

    def post(self):
        url_string = str(self.request.url)
        url_obj = urlparse.urlparse(url_string)
        # str.split returns a list of strings. Google search python str.split for more detail.
        subdirs = str(url_obj.path).split('/')
        # Last element in the url
        last_dir_string = str(subdirs[len(subdirs)-1])
        num_layers = len(subdirs)

        if num_layers == 2 and last_dir_string == "dish":
            err, req_params = utils.validate_data(self.request)
            if err:
                self.response.out.write(err.message())
                return
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
                handling_function = post_sub_routes[last_dir_string]
                self = getattr(CommentHandler, handling_function)(self)
                return
            except KeyError:
                self.response.out.write("Invalid URL")
                return

    def put(self):
        url_string = str(self.request.url)
        url_obj = urlparse.urlparse(url_string)
        # str.split returns a list of strings. Google search python str.split for more detail.
        subdirs = str(url_obj.path).split('/')
        # Last element in the url
        action = str(subdirs[len(subdirs)-2])
        dish_id = str(subdirs[len(subdirs)-1])
        # TO-DO: Add error checking and handling
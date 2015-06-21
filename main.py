import cgi
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import utils
import errors
import json
import MySQLdb
import os
import jinja2

# Configure the Jinja2 environment.
# Define your production Cloud SQL instance information.
_INSTANCE_NAME = 'fiidup-sql:fiidup-db'
#db = MySQLdb.connect(host='173.194.107.106', port=3306, db='fiidup_main', user='root', charset='utf 8')
##db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='fiidup_main', user='root', charset='utf 8')

class MainPage(webapp2.RequestHandler):
    def get(self):
        logging.info("Hello")

    def post(self):
        error, req_params = utils.validate_data(self.request)
        if error:
            self.response.out.write(error.message())
            return
        logging.info(json.dumps(req_params))

class Dish(webapp2.RequestHandler):
    def post(self):
        # Handle the post to create a new guestbook entry.
        dish_name = self.request.get('dish_name')
        restaurant_id = self.request.get('restaurant_id')
        user_id = self.request.get('user_id')
        url = self.request.get('url')
        posted_time = self.request.get('posted_time')
        price = self.request.get('price')
        tags = self.request.get('tags')
        longitude = 0.0000
        latitude = 0.0000

        cursor = db.cursor()

        # Note that the only format string supported is %s
        cursor.execute('INSERT INTO dish (dish_name, restaurant_id, user_id, caption, url, posted_time, price, tags, like_count, comment_count) VALUES (%s, %s)', (fname, content))
        db.commit()

        self.redirect("/")

application = webapp2.WSGIApplication([('/', MainPage),
                               ('/sign', Dish)],
                              debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
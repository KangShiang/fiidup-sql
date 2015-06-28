import logging
import json
import global_vars

import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import utils

from Dish import Dish as DishHandler
from Restaurant import Restaurant as RestaurantHandler
# Define your production Cloud SQL instance information.

class MainPage(webapp2.RequestHandler):
    def get(self):
        logging.info("Hello")

    def post(self):
        error, req_params = utils.validate_data(self.request)
        if error:
            self.response.out.write(error.message())
            return
        logging.info(json.dumps(req_params))

application = webapp2.WSGIApplication([('/', MainPage),
                               ('/dish.*', DishHandler.Dish),
                               ('/restaurant.*', RestaurantHandler.Restaurant)],

                              debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
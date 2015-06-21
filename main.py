import cgi
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import utils
import json
import MySQLdb
import os
import jinja2

# Configure the Jinja2 environment.
# Define your production Cloud SQL instance information.
_INSTANCE_NAME = 'fiidup-sql:fiidup-db'
db = MySQLdb.connect(host='173.194.107.106', port=3306, db='fiidup_main', user='all')
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
        err, req_params = utils.validate_data(self.request)
        if err:
            self.response.out.write(err.message())
            return
        placeholders = ', '.join(['%s'] * len(req_params))
        columns = ', '.join(req_params.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("dish", columns, placeholders)
        test = (sql, req_params.values())
        logging.info(test)
        cursor = db.cursor()
        # Note that the only format string supported is %s
        try:
            cursor.execute(sql, req_params.values())
            db.commit()
        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))

        self.response.out.write(json.dumps(req_params))

application = webapp2.WSGIApplication([('/', MainPage),
                               ('/dish', Dish)],
                              debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
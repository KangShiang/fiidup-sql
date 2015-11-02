import webapp2
import urlparse
import MySQLdb
import sql
import utils

class Username(webapp2.RequestHandler):
    def get(self):
        url_obj = urlparse.urlparse(str(self.request.url))
        subdirs = str(url_obj.path).split('/')
        num_layers = len(subdirs)
        username = str(subdirs[len(subdirs)-1])

        if num_layers == 3:
            data = None
            error = None
            cursor = sql.db.cursor()
            try:
                condition = {'username': username}
                data = {'username': username}
                query_string = sql.get_retrieve_query_string(table='person', cond=condition)
                cursor.execute(query_string)
                data['status'] = 'unavailable' if cursor.fetchall() else 'available'
            except MySQLdb.Error, e:
                error = sql.get_sql_error(e)
                self.response.status = 403
            cursor.close()
            self.response.out.write(utils.generate_json(self.request, None, 'GET', data, error))
        else:
            self.response.status = 405

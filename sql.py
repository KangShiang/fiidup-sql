import errors
import logging
import MySQLdb

_INSTANCE_NAME = 'fiidup-sql:fiidup-db'
db = MySQLdb.connect(host='173.194.107.106', port=3306, db='fiidup_main', user='all')
##db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='fiidup_main', user='root', charset='utf 8')


def get_insert_query_string(table, params):
    logging.info(params)
    query = "INSERT INTO " + table + " ("
    values = []
    for key in params.keys():
        query = query + key + ", "
        values.append(params[key])
    query = query[:-2]
    query += ") VALUES ("
    for x in values:
        try:
            int(x)
            query = query + x + ", "
        except ValueError:
            if 'GeomFromText' in x:
                query = query + x + ", "
            else:
                query = query + '"' + x + '", '

    query = query[:-2] + ")"
    logging.info(query)
    return query

def get_modify_query_string(table, params, primary_key, id):
    query = "UPDATE " + table + " SET"
    for key, value in params.iteritems():
        if key != primary_key:
            try:
                int(value)
                query = query + " " + key + "=" + value + ","
            except ValueError:
                if 'GeomFromText' in value:
                    query = query + " " + key + "=" + value + ", "
                else:
                    query = query + " " + key + "=\"" + value + "\", "
    query = query[:-2] + " where " + primary_key + "=" + id + ";"
    logging.info(query)

    return query
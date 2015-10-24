import re
import logging
import MySQLdb

#db = MySQLdb.connect(host='173.194.107.106', port=3306, db='fiidup_main', user='all')
#db = MySQLdb.connect(host='localhost', port=3306, db='fiidup_main', user='all')
db = MySQLdb.connect(host='localhost', port=3306, db='fiidup_main', user='root', passwd='root')

def is_int(x):
    try:
        int(x)
    except ValueError:
        return False
    return True

# TODO: queries may be susceptible to sql injection when exposed!!!
# Consider validating data: remove dangerous characters

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
        if is_int(x):
            query = query + x + ", "
        else:
            if 'GeomFromText' in x:
                query = query + x + ", "
            else:
                query = query + '"' + x + '", '

    query = query[:-2] + ")"
    logging.info(query)
    return query

def get_retrieve_query_string(table, params=None, cond=None, limit=None):
    """
    Function to query data from the database, with exact matching conditions
    table is the table to query FROM
    params if specified, should have a list of columns to SELECT
    eg: params = ['dish_name', 'restaurant_id']
    if params is not specified or is empty, SELECT *
    cond if specified, should have a dictionary of key, value pairs as the WHERE clause
    limit if specified, indicates the LIMIT in integer, default None
    eg: cond = {'dish_name': 'Cake', 'like_count': 0, 'dish_id': [123, 345]}
    """
    logging.info(params)
    query = "SELECT "
    if (params is None) or len(params) == 0:
        if table == "dish" or table == "restaurant":
            params = get_column_names(table)
        else:
            query += " *   "    # last 2 spaces will always be removed
            params = []

    for param in params:
        if param == 'location':
            query = query + "AsText(" + param + "), "
        else:
            query = query + param + ", "
    query = query[:-2]
    query = query + " FROM " + table
    if (cond is not None) and len(cond) > 0:
        query += " WHERE "
        for key in cond.keys():
            if type(cond[key]) is list:
                query = query + "(" + key + " IN ("
                for element in cond[key]:
                    if is_int(element):
                        query = query + str(element) + ", "
                    else:
                        query = query + "'" + element + "', "
                query = query[:-2] + ")) AND "
            elif is_int(cond[key]):
                query = query + "(" + key + " = " + str(cond[key]) + ") AND "
            else:
                query = query + "(" + key + " = '" + cond[key] + "') AND "
        query = query[:-5]
    if limit is not None:
        query = query + " LIMIT " + str(limit)
    logging.info(query)
    return query

def get_retrieve_numeric_query_string(table, params=None, cond=None, limit=None):
    """
    Function to query data from the database, with numeric operations
    table is the table to query FROM
    params if specified, should have a list of columns to SELECT
    eg: params = ['dish_name', 'restaurant_id']
    if params is not specified or is empty, SELECT *
    cond if specified, should have a dictionary of key, value pairs as the WHERE clause
    cond must be numeric, contains the operator, formatted as a string
    limit if specified, indicates the LIMIT, default None
    eg: cond = {'like_count': '< 10', 'comment_count': '> 20', 'tasted_count': '= 50'}
    """
    logging.info(params)
    query = "SELECT "
    if (params is None) or len(params) == 0:
        if table == "dish" or table == "restaurant":
            params = get_column_names(table)
        else:
            query += " *   "    # last 2 spaces will always be removed
            params = []
    for param in params:
        if param == 'location':
            query = query + "AsText(" + param + "), "
        else:
            query = query + param + ", "
    query = query[:-2]
    query = query + " FROM " + table
    if (cond is not None) and len(cond) > 0:
        query += " WHERE "
        for key in cond.keys():
            query = query + "(" + key + " " + cond[key] + ") AND "
        query = query[:-5]
    if limit is not None:
        query = query + " LIMIT " + str(limit)
    logging.info(query)
    return query

def generate_location_range(axis, min, max):
    """
    Function to generate 1 dictionary key, value pair which can be added to cond
    * use dict.update(dict2) to update existing dict
    axis either 'X' or 'Y'; specifies longitude or latitude
    min and max are signed integers
    Returns one dictionary element
    eg: {'X(location)': 'BETWEEN 25 AND 50'}
    If axis, min or max is invalid, None will be returned
    """
    if min > max:
        return None
    temp = 'BETWEEN ' + str(min) + ' AND ' + str(max)
    if axis == 'X':
        # check for valid longtitude (-180 to 180)
        if (-180 < min < 180) and (-180 < max < 180):
            return {'X(location)': temp}
    elif axis == 'Y':
        # check for valid latitude (-90 to 90)
        if (-90 < min < 90) and (-90 < max < 90):
            return {'Y(location)': temp}
    return None

def get_modify_query_string(table, params, primary_key, id):
    """
    Function to generate a query string which updates an entry in the table
    based on the primary_key
    :type table: str
    :type params: dict
    :type primary_key: str
    :type id: str
    """
    query = "UPDATE " + table + " SET "
    for key, value in params.iteritems():
        if key != primary_key:
            if re.search('[+-]', str(value)) is not None:
                query = query + key + "=" + str(value) + ", "
            elif type(value) is int:
                query = query + key + "=" + value + ", "
            else:
                if 'GeomFromText' in value:
                    query = query + key + "=" + value + ", "
                else:
                    query = query + key + "='" + value + "', "
    query = query[:-2] + " where " + primary_key + "=" + id + ";"
    logging.info(query)
    return query

def get_delete_query_string(table, primary_key, value):
    """
    Function to generate a query string which deletes an entry in the table
    based on the primary_key and the corresponding value
    """
    query = "DELETE FROM " + str(table)
    query += " WHERE " + str(primary_key) + " = " + str(value)
    logging.info(query)
    return query

def get_column_names(table):
    """
    Function to return the entire list of column names from input table
    """
    cursor = db.cursor()
    cursor.execute("DESCRIBE %s;" % table)
    keys = [x[0] for x in cursor.fetchall()]
    cursor.close()
    return keys

def get_last_inserted_pkey(cursor):
    return cursor.lastrowid

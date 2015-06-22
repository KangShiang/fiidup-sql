import errors
import logging

def get_insert_query_string(table, params):
    logging.info(params)
    query = "INSERT INTO " + table + " ("
    values = []
    for key in params.keys():
        query = query + key + ", "
        values.append(params[key])
    query = query[:-2]
    query = query + ") VALUES ("
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
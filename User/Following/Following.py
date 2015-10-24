import MySQLdb
import json
import sql
import utils
import logging


def put_following(handler, id, params):
    """
    :param id: The id of target user to be inserted
    """
    data = None
    error = None
    cursor = sql.db.cursor()
    # get this user id
    this_user = utils.get_user(handler.request, handler.response)
    if this_user is None:
        cursor.close()
        error = "You do not have a user id. Good bye..."
        return data, error
    if id:
        try:
            # obtain following dict of this user
            cond = {'user_id': this_user}
            query = sql.get_retrieve_query_string(table='following', cond=cond)
            cursor.execute(query)
            following_dict = cursor.fetchall()[0][1]
            following_dict = json.loads(cursor.fetchall()[0][1]) if following_dict is not None else {}
            # obtain the follower dict of target user
            cond = {'user_id': id}
            query = sql.get_retrieve_query_string(table='follower', cond=cond)
            cursor.execute(query)
            follower_dict = cursor.fetchall()[0][1]
            follower_dict = json.loads(cursor.fetchall()[0][1]) if follower_dict is not None else {}
            # obtain the username of the target id
            cond = {'user_id': int(id)}
            param = ['username']
            query = sql.get_retrieve_query_string(table='person', params=param, cond=cond)
            cursor.execute(query)
            username = cursor.fetchall()[0][0]
            # add the target user to the following dict of this user
            following_dict[id] = username
            # add this user from the follower dict of the target user
            follower_dict[this_user] = username
            # update following table
            param = {'following': json.dumps(following_dict)}
            query = sql.get_modify_query_string('following', param, 'user_id', this_user)
            cursor.execute(query)
            # update follower table
            param = {'follower': json.dumps(follower_dict)}
            query = sql.get_modify_query_string('follower', param, 'user_id', id)
            cursor.execute(query)
            sql.db.commit()
            data = {'user_id': id}

        except KeyError, e:
            logging.error("Invalid key specified for deletion: %s" % e)
            error = "Invalid key specified for deletion: %s" % e
            handler.response.status = 403

        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            sql.db.rollback()
            handler.response.status = 403
    else:
        error = "No target user id specified"
        handler.response.status = 403

    cursor.close()
    logging.info(data)
    return data, error

def get_following(handler, id, params):
    data = None
    error = None
    cursor = sql.db.cursor()
    user_id = utils.get_user(handler.request, handler.response)
    if user_id is None:
        cursor.close()
        error = "You do not have a user id. Good bye..."
        return data, error
    if id:
        # obtain the following dict of the user with id
        user_id = str(id)
    try:
        cond = {'user_id': user_id}
        query = sql.get_retrieve_query_string(table='following', cond=cond)
        cursor.execute(query)
        # converting dict string to dict[user_id, username]
        following_dict = cursor.fetchall()[0][1]
        following_dict = json.loads(cursor.fetchall()[0][1]) if following_dict is not None else {}
        data = following_dict

    except MySQLdb.Error, e:
        try:
            logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            logging.error("MySQL Error: %s" % str(e))
            error = "MySQL Error: %s" % str(e)
        handler.response.status = 403
    cursor.close()
    logging.info(data)
    return data, error

def delete_following(handler, id, params):
    """
    :param id: The id of target user to be deleted
    """
    data = None
    error = None
    cursor = sql.db.cursor()
    # get this user id
    this_user = utils.get_user(handler.request, handler.response)
    if this_user is None:
        cursor.close()
        error = "You do not have a user id. Good bye..."
        return data, error
    if id:
        try:
            # obtain following dict of this user
            cond = {'user_id': this_user}
            query = sql.get_retrieve_query_string(table='following', cond=cond)
            cursor.execute(query)
            following_dict = cursor.fetchall()[0][1]
            following_dict = json.loads(cursor.fetchall()[0][1]) if following_dict is not None else {}
            # obtain the follower dict of target user
            cond = {'user_id': id}
            query = sql.get_retrieve_query_string(table='follower', cond=cond)
            cursor.execute(query)
            follower_dict = cursor.fetchall()[0][1]
            follower_dict = json.loads(cursor.fetchall()[0][1]) if follower_dict is not None else {}
            # delete the target user from the following dict of this user
            del following_dict[id]
            # delete this user from the follower dict of the target user
            del follower_dict[this_user]
            # update following table
            param = {'following': json.dumps(following_dict)}
            query = sql.get_modify_query_string('following', param, 'user_id', this_user)
            cursor.execute(query)
            # update follower table
            param = {'follower': json.dumps(follower_dict)}
            query = sql.get_modify_query_string('follower', param, 'user_id', id)
            cursor.execute(query)
            sql.db.commit()
            data = {'user_id': id}

        except KeyError, e:
            logging.error("Invalid key specified for deletion: %s" % e)
            error = "Invalid key specified for deletion: %s" % e
            handler.response.status = 403

        except MySQLdb.Error, e:
            try:
                logging.error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                error = "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                logging.error("MySQL Error: %s" % str(e))
                error = "MySQL Error: %s" % str(e)
            sql.db.rollback()
            handler.response.status = 403
    else:
        error = "No target user id specified"
        handler.response.status = 403

    cursor.close()
    logging.info(data)
    return data, error

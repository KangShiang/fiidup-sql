import MySQLdb
import json
import sql
import utils
import logging


def put_following(handler, this_user, params):
    data = None
    error = None
    cursor = sql.db.cursor()
    target_user = params['user_id']
    if this_user == int(target_user):
        error = "Invalid user_id specified for insertion: %s" % target_user
        handler.response.status = 403
    else:
        try:
            # obtain following dict of this user
            cond = {'user_id': this_user}
            query = sql.get_retrieve_query_string(table='following', cond=cond)
            cursor.execute(query)
            following_dict = cursor.fetchall()[0][1]
            following_dict = json.loads(following_dict) if following_dict is not None else {}
            # obtain the follower dict of target user
            cond = {'user_id': target_user}
            query = sql.get_retrieve_query_string(table='follower', cond=cond)
            cursor.execute(query)
            follower_dict = cursor.fetchall()[0][1]
            follower_dict = json.loads(follower_dict) if follower_dict is not None else {}
            # obtain the username of the target id
            cond = {'user_id': target_user}
            query = sql.get_retrieve_query_string(table='person', params=['username'], cond=cond)
            cursor.execute(query)
            username = cursor.fetchall()[0][0]
            # add the target user to the following dict of this user
            following_dict[str(target_user)] = username
            # add this user from the follower dict of the target user
            follower_dict[str(this_user)] = username
            # update following table
            param = {'following': json.dumps(following_dict)}
            query = sql.get_modify_query_string('following', param, 'user_id', this_user)
            cursor.execute(query)
            # update follower table
            param = {'follower': json.dumps(follower_dict)}
            query = sql.get_modify_query_string('follower', param, 'user_id', target_user)
            cursor.execute(query)
            sql.db.commit()
            data = {'user_id': target_user}
        except IndexError:
                error = "Invalid user_id specified for insertion: %s" % target_user
                handler.response.status = 403
        except MySQLdb.Error, e:
            error = sql.get_sql_error(e)
            handler.response.status = 403
    cursor.close()
    logging.info(data)
    handler.response.out.write(utils.generate_json(handler.request, this_user, "PUT", data, error))

def get_following(handler, this_user, target_user):
    # User id is always passed in as id
    data = None
    error = None
    cursor = sql.db.cursor()
    cond = {'user_id': target_user}
    try:
        query = sql.get_retrieve_query_string(table='following', cond=cond)
        cursor.execute(query)
        following_dict = cursor.fetchall()[0][1]
        following_dict = json.loads(following_dict) if following_dict is not None else {}
        data = following_dict
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        handler.response.status = 403
    cursor.close()
    logging.info(data)
    handler.response.out.write(utils.generate_json(handler.request, this_user, "GET", data, error))

def delete_following(handler, this_user, target_user):
    data = None
    error = None
    cursor = sql.db.cursor()
    try:
        # obtain following dict of this user
        cond = {'user_id': this_user}
        query = sql.get_retrieve_query_string(table='following', cond=cond)
        cursor.execute(query)
        following_dict = cursor.fetchall()[0][1]
        following_dict = json.loads(following_dict) if following_dict is not None else {}
        # obtain the follower dict of target user
        cond = {'user_id': target_user}
        query = sql.get_retrieve_query_string(table='follower', cond=cond)
        cursor.execute(query)
        follower_dict = cursor.fetchall()[0][1]
        follower_dict = json.loads(follower_dict) if follower_dict is not None else {}
        # delete the target user from the following dict of this user
        del following_dict[str(target_user)]
        # delete this user from the follower dict of the target user
        del follower_dict[str(this_user)]
        # update following table
        param = {'following': json.dumps(following_dict)}
        query = sql.get_modify_query_string('following', param, 'user_id', this_user)
        cursor.execute(query)
        # update follower table
        param = {'follower': json.dumps(follower_dict)}
        query = sql.get_modify_query_string('follower', param, 'user_id', target_user)
        cursor.execute(query)
        sql.db.commit()
        data = {'user_id': target_user}
    except KeyError, e:
        error = "Invalid user_id specified for deletion: %s" % e
        handler.response.status = 403
    except IndexError:
        error = "Invalid user_id specified for deletion: %s" % target_user
        handler.response.status = 403
    except MySQLdb.Error, e:
        error = sql.get_sql_error(e)
        handler.response.status = 403
    cursor.close()
    logging.info(data)
    handler.response.out.write(utils.generate_json(handler.request, this_user, "PUT", data, error))

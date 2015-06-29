from datetime import datetime
import Profile as profile_lib
import json
from google.appengine.ext import ndb

class UserModel(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    profile = ndb.StringProperty()
    fiider_count = ndb.IntegerProperty()
    fiiding_count = ndb.IntegerProperty()
    post_count = ndb.IntegerProperty()

# User class is created when signing up or logging in
class User(object):
    # User object constructor
    def __init__(self, username, password, profile, ID):
        self.username = username
        self.password = password
        self.profile = profile
        self.id = ID
        self.fiider_count = None		# These 3 parameters are set to 0 upon sign up
        self.fiiding_count = None		# These values are fetched from the datastore upon login
        self.post_count = None

    # This method checks if the username provided by the user already exists. If the username exists
    # this method returns -1, else it stores the user in the datastore and returns the userid of the user.
    def sign_up(self):
        if not self.datastore_check_for_username():
            self.id = self.datastore_put()
        else:
            self.id = "-1"

    # This method check if the user's username and password match with the datastore entry.
    # If none of the entry matches, it returns a -1. Else, it returns true. "self" contains the actually logged in user.
    def log_in(self):
        # TODO: Need to get the key ID from the server
        if self.datastore_check_for_user():
            return
        else:
            self.id = "-1"

    # Storing the user object into the datastore. This method assumes the object has been created ahead of time
    # before the method is called.
    # This method is used for signing up
    def datastore_put(self):
        profile_obj = {
            'location'   : self.profile.location,
            'age'        : self.profile.age,
            'gender'     : self.profile.gender,
            'signupdate' : self.profile.signupdate
        }
        user = UserModel(username = self.username, password = self.password, profile = json.dumps(profile_obj),
                              fiider_count = 0, fiiding_count = 0, post_count = 0)
        key = user.put()
        return str(key.id())

    # This method check for existing username.
    def datastore_check_for_username(self):
        user_query = UserModel.query(UserModel.username == self.username)
        users = user_query.fetch()
        # If no data was found, store the object as an entry in the datastore
        if len(users) == 0:
            return False
        else:
            return True

    # This method checks for existing username and password
    # Fetches user data if exists
    def datastore_check_for_user(self):
        user_query = UserModel.query(UserModel.username == self.username, UserModel.password == self.password)
        users = user_query.fetch()

        # If no data was found, store the object as an entry in the datastore
        if len(users) == 0:
            return False
        else:
            self.username = users[0].username
            self.password = users[0].password
            self.id = str(users[0].key.id())
            temp_profile = json.loads(users[0].profile)
            self.profile = profile_lib.Profile(location=temp_profile['location'], age = temp_profile['age'],
                                               gender = temp_profile['gender'], signupdate = temp_profile['signupdate'])
            self.fiider_count = users[0].fiider_count
            self.fiiding_count = users[0].fiiding_count
            self.post_count = users[0].post_count
            return True

    # The user info given by self.id will be fetched from the datastore and loaded onto self
    # Returns true if info exists, false otherwise
    def datastore_fetchUserInfo(self):
        try:
            user = UserModel.get_by_id(int(self.id))
        # exception when self.id is an invalid int
        except ValueError:
            user = None

        if user is None:
            return False
        else:
            self.username = user.username
            self.password = ''		# suppress visibility of password
            temp_profile = json.loads(user.profile)
            self.profile = profile_lib.Profile(location = temp_profile['location'], age = temp_profile['age'],
                                               gender = temp_profile['gender'], signupdate = temp_profile['signupdate'])
            self.fiider_count = user.fiider_count
            self.fiiding_count = user.fiiding_count
            self.post_count = user.post_count
            return True

class Profile:
    # Profile class constructor
    def __init__(self, location, age, gender, signupdate):
        self.location = location
        self.age = age
        self.gender = gender
        self.signupdate = signupdate

    def __dir__(self):
            return ['location', 'age', 'gender', 'signupdate']

    def objectify(self, temp_profile):
        obj = {
            'location'   : temp_profile.location,
            'age'        : temp_profile.age,
            'gender'     : temp_profile.gender,
            'signupdate' : temp_profile.signupdate
        }
        return obj

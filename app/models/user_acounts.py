class UserAccounts:
    """
    Blue print for creating and managing users
    Contains user accounts attributes method
    It will be responsible for displaying all events
    """

    def __init__(self):
        self.users = {}
        self.events = []

    # Add a new user into the database
    def create_user(self, user):
        if user.id in self.users:
            raise KeyError("There exists a user with that name. Please use another name")
        else:
            return self.users.update({user.id: user})

    # Return a specific user
    def get_specific_user(self, username):
        if username in self.users:
            return self.users[username]
        else:
            raise KeyError("The user does not exist")

    # Delete a user
    def delete_user(self, username):
        try:
            self.users.pop(username)
        except KeyError:
            print("The User does not exist")
            raise
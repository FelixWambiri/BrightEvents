def search():
    """
    This search method is work in progress
    It is made global so that it can be used in other class models
    :return:
    """


class Attendants:
    """
    Blue print for creating an event attendee
    """
    def __init__(self, name, email, contacts):
        self.name = name
        self.email = email
        self.contacts = contacts

        
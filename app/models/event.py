class Event:
    """
    This class is the blueprint for creating an event
    It avails the attributes required for an event
    """
    def __init__(self, name, category, location, owner):
        self.name = name
        self.category = category
        self.location = location
        self.owner = owner
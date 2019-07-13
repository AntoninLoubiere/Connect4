class Preferences(object):
    """
    A preferences class
    """

    def __init__(self):
        """
        Constructor
        """
        self.temporary_preferences = {}

    def set_temporary_preference(self, key, value):
        """
        Set a temporary global preference to a value
        :param key: The key of the variable
        :param value: The value of the variable
        :return: None
        """

        self.temporary_preferences[key] = value

    def get_temporary_preference(self, key):
        """
        Get a temporary preference
        :param key: The key of the preference
        :return: the value of the preference
        """

        try:
            return self.temporary_preferences[key]
        except KeyError:
            print("WARNING: " + str(key) + " don't exist !")
            return None

    def remove_temporary_preference(self, key):
        """
        Remove a temporary preference
        :param key: The key
        :return: None
        """
        try:
            del self.temporary_preferences[key]
        except KeyError:
            print("WARNING: " + str(key) + "don't exist !")
            return None

    def temporary_preference_exist(self, key):
        """
        Test if a preference temporary exist
        :param key: The key of the preference
        :return: None
        """
        return key in self.temporary_preferences

import os
import pickle

SAVING_FILE = "preferences.pkl"

PREFERENCE_CURRENT_LANGUAGE = 0  # use int not str to save memory
DEFAULT_LANGUAGE = "EN_en"
PREFERENCE_DELAY = 1
DEFAULT_DELAY = 500
DELAY_MIN = 0
DELAY_MAX = 5000
PREFERENCE_DIFFICULTY_LEVEl = 2
DEFAULT_DIFFICULTY_LEVEL = [1, 3, 4, 5, 6, 7]
DIFFICULTY_LEVEL_MIN = 1
DIFFICULTY_LEVEL_MAX = 15

DEFAULT_PREFERENCES = {
    PREFERENCE_DELAY: DEFAULT_DELAY,
    PREFERENCE_DIFFICULTY_LEVEl: DEFAULT_DIFFICULTY_LEVEL
}

TEMPORARY_PREFERENCES_PLAYERS_TOKENS = 0
TEMPORARY_PREFERENCES_PLAYERS_AI = 1
TEMPORARY_PREFERENCES_PLAYERS_NAMES = 2
TEMPORARY_PREFERENCES_DIFFICULTY = 3


class Preferences(object):
    """
    A preferences class
    """

    def __init__(self, default_preferences=None, default_temporary_preferences=None):
        """
        Constructor
        """
        if default_temporary_preferences is None:
            default_temporary_preferences = {}
        if default_preferences is None:
            default_preferences = {}

        self.temporary_preferences = default_temporary_preferences
        self.preferences = {}

        self.default_preferences = default_preferences
        self.default_temporary_preferences = default_temporary_preferences

        self.load_preferences()

        for key in default_preferences:
            if not self.preference_exist(key):
                self.set_preference(key, self.default_preferences[key])

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

    def reset_default_values_temporary_preferences(self):
        """
        Reset the preference with default values
        :return: None
        """

        for key in self.default_temporary_preferences:
            self.set_temporary_preference(key, self.default_temporary_preferences[key])

    def load_preferences(self):
        """
        Load all preferences
        :return: None
        """
        try:
            if os.path.exists(SAVING_FILE):
                with open(SAVING_FILE, 'rb') as fir:
                    self.preferences = pickle.load(fir)

        except pickle.PickleError:
            self.preferences = {}

    def save_preferences(self):
        """
        Save all preferences
        :return: None
        """
        try:
            with open(SAVING_FILE, 'wb') as fir:
                pickle.dump(self.preferences, fir)

        except pickle.PickleError:
            pass

    def set_preference(self, key, value):
        """
        Set a permanent global preference to a value
        :param key: The key of the variable
        :param value: The value of the variable
        :return: None
        """

        self.preferences[key] = value

    def get_preference(self, key):
        """
        Get a permanent preference
        :param key: The key of the preference
        :return: the value of the preference
        """

        try:
            return self.preferences[key]
        except KeyError:
            print("WARNING: " + str(key) + " don't exist !")
            return None

    def remove_preference(self, key):
        """
        Remove a permanent preference
        :param key: The key
        :return: None
        """
        try:
            del self.preferences[key]
        except KeyError:
            print("WARNING: " + str(key) + "don't exist !")
            return None

    def preference_exist(self, key):
        """
        Test if a preference permanent exist
        :param key: The key of the preference
        :return: None
        """
        return key in self.preferences

    def reset_default_values_preference(self):
        """
        Reset the preference with default values
        :return: None
        """

        for key in self.default_preferences:
            self.set_preference(key, self.default_preferences[key])

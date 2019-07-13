import TokenState


class Player(object):
    """
    The class of players
    """

    def __init__(self, player_enum, token, name=None):
        """
        Constructor
        :param player_enum: the token state to know which player is
        :param token: the token color of the player
        :param name: the name of the player
        """

        self.player_enum = player_enum
        self.token = token

        if name is None:
            self.name = ("Player 2", "Player 1")[player_enum == TokenState.TokenState.Player_1]
        else:
            self.name = name

    def get_thinking(self):
        """
        Function for AI class (see AI class)
        :return: See AI class
        """

        raise NotImplementedError("You must use this function with a AI class")

    def run_turn(self):
        """
        Function for AI class (see AI class)
        :return: See AI class
        """

        raise NotImplementedError("You must use this function with a AI class")

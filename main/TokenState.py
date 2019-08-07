import enum


class TokenState(enum.Enum):
    """
    An enum, the state of tiles
    """

    Blank = 0
    Player_1 = 1
    Player_2 = 2

    @staticmethod
    def get_opponent(player):
        """
        Get the opponent player of a player
        :param player: the player
        :return: None
        """
        if player == TokenState.Player_1:
            return TokenState.Player_2
        elif player == TokenState.Player_2:
            return TokenState.Player_1
        else:
            raise RuntimeError("Can't find the opponent player")

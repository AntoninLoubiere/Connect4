from TileState import TileState
import random


GRID_WIDTH = 7
GRID_HEIGHT = 6


class Game(object):
    """
    A class to save some variables (the grid...). It represent a game
    """

    def __init__(self):
        """
        Constructor
        """

        self.grid = []
        for x in range(GRID_WIDTH):
            self.grid.append([])
            for y in range(GRID_HEIGHT):
                self.grid[x].append(TileState.Blank)

        self.current_turn = (TileState.Player_1, TileState.Player_2)[random.randint(0, 1) == 0]

    def add_tile(self, column):
        """
        Add the tile of the current player in a column
        :param column: the column which you would add the tile
        :return: if this action was do
        """

        for y in range(len(self.grid[column]) - 1, 0 - 1, -1):
            if self.grid[column][y] == TileState.Blank:
                #  add tile
                self.grid[column][y] = self.current_turn
                self.swap_turn()
                return True

        return False

    def swap_turn(self):
        """
        Swap the turn (Player 1 to 2 and 2 to 1)
        :return: None
        """
        self.current_turn = (TileState.Player_1, TileState.Player_2)[self.current_turn == TileState.Player_1]

    def __str__(self):
        """
        Return grid status
        :return: string which contain a status to print
        """
        string = "Grid: \n"

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                string += "{:^8}".format(self.grid[x][y].name)
                string += (" | ", "\n")[x == GRID_WIDTH - 1] # if is the last element

        string += "\nLe tour est à: " + self.current_turn.name

        return string

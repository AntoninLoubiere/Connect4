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
        for y in range(0, GRID_HEIGHT):
            self.grid.append([])
            for x in range(0, GRID_WIDTH):
                self.grid[y].append(TileState.Blank)

        self.current_turn = (TileState.Player_1, TileState.Player_2)[random.randint(0, 1) == 0]

    def __str__(self):
        """
        Return grid status
        :return: string which contain a status to print
        """
        string = "Grid: \n"

        for iy, y in enumerate(self.grid):
            for ix, x in enumerate(y):
                string += "{:^8}".format(x.name)
                string += (" | ", "\n")[ix == len(y) - 1]

        string += "\nLe tour est à: " + self.current_turn.name

        return string

import random
import time

from main.TokenState import TokenState


class Game(object):
    """
    A class to save some variables (the grid...). It represent a game
    """

    def __init__(self, grid_width=7, grid_height=6,
                 first_player=None):
        """
        Constructor
        """

        self.grid = []

        self.grid_width = grid_width
        self.grid_height = grid_height

        for x in range(self.grid_width):
            self.grid.append([])
            for y in range(self.grid_height):
                self.grid[x].append(TokenState.Blank)

        if first_player is None:
            self.current_turn = (TokenState.Player_1, TokenState.Player_2)[random.randint(0, 1)]
        else:
            self.current_turn = first_player

        self.game_win = False
        self.winner = TokenState.Blank
        self.win_tokens_coord = [[-1, -1], [-1, -1]]

        self.score = [0, 0]

    def add_token(self, column):
        """
        Add the token of the current player in a column
        :param column: the column which you would add the token
        :return: 0: if this action was do 1: a list with coord of the token
        """
        if self.is_win():
            return [False, [-1, -1]]

        for y in range(self.grid_height - 1, -1, -1):
            if self.grid[column][y] == TokenState.Blank:
                #  add token
                self.grid[column][y] = self.current_turn
                self.swap_turn()
                self.update_win(column, y)
                return [True, [column, y]]

        return [False, [-1, -1]]

    def add_token_with_coord(self, x, y):
        """
        Add the token of the current player at coord
        :param x: The x coord of the new token
        :param y: The y coord of the new token
        :return: 0: if this action was do 1: a list with coord of the token
        """
        if self.is_win():
            return [False, [-1, -1]]
        print(x,y)
        if self.grid[x][y] == TokenState.Blank and (y == self.grid_height - 1 or self.grid[x][y + 1] !=
                                                    TokenState.Blank):
            #  add token
            self.grid[x][y] = self.current_turn
            self.swap_turn()
            self.update_win(x, y)
            return [True, [x, y]]

        else:
            return [False, [-1, -1]]

    def swap_turn(self):
        """
        Swap the turn (Player 1 to 2 and 2 to 1)
        :return: None
        """
        self.current_turn = (TokenState.Player_1, TokenState.Player_2)[self.current_turn == TokenState.Player_1]

    def update_win(self, x, y):
        """
        Update the win of the token in parameter
        :param x: The x of the token to check
        :param y: The y of the token to check
        :return: If anybody win
        """

        number_align = 1  # current number
        temp_coord = [[x, y], [x, y]]  

        # #Test column#

        # count bottom
        for current_y in range(y + 1, self.grid_height):
            if self.grid[x][current_y] != self.grid[x][y]:
                break

            number_align += 1
            temp_coord[0] = [x, current_y]

        # count top
        for current_y in range(y - 1, -1, -1):
            if self.grid[x][current_y] != self.grid[x][y]:
                break

            number_align += 1
            temp_coord[1] = [x, current_y]

        if number_align >= 4:
            self.set_winner(self.grid[x][y])
            self.win_tokens_coord = temp_coord
            return True

        number_align = 1 
        temp_coord = [[x, y], [x, y]]

        # #Test row#

        # count right
        for current_x in range(x + 1, self.grid_width):
            if self.grid[current_x][y] != self.grid[x][y]:
                break

            number_align += 1
            temp_coord[0] = [current_x, y]

        # count left
        for current_x in range(x - 1, -1, -1):
            if self.grid[current_x][y] != self.grid[x][y]:
                break

            number_align += 1
            temp_coord[1] = [current_x, y]

        if number_align >= 4:
            self.set_winner(self.grid[x][y])
            self.win_tokens_coord = temp_coord
            return True

        number_align = 1 
        temp_coord = [[x, y], [x, y]]

        # #Test diagonal top left - bottom right#

        # count bottom right
        current_x = x + 1
        current_y = y + 1

        while current_x < self.grid_width and current_y < self.grid_height:
            if self.grid[current_x][current_y] != self.grid[x][y]:
                break

            temp_coord[0] = [current_x, current_y]
            current_x += 1
            current_y += 1
            number_align += 1

        # count top left
        current_x = x - 1
        current_y = y - 1

        while current_x >= 0 and current_y >= 0:
            if self.grid[current_x][current_y] != self.grid[x][y]:
                break

            temp_coord[1] = [current_x, current_y]
            current_x -= 1
            current_y -= 1
            number_align += 1

        if number_align >= 4:
            self.set_winner(self.grid[x][y])
            self.win_tokens_coord = temp_coord
            return True

        # #Test diagonal top right - bottom left#

        number_align = 1 
        temp_coord = [[x, y], [x, y]]

        # count top right
        current_x = x + 1
        current_y = y - 1

        while current_x < self.grid_width and current_y >= 0:
            if self.grid[current_x][current_y] != self.grid[x][y]:
                break

            temp_coord[0] = [current_x, current_y]
            current_x += 1
            current_y -= 1
            number_align += 1

        # count bottom left
        current_x = x - 1
        current_y = y + 1

        while current_x >= 0 and current_y < self.grid_height:
            if self.grid[current_x][current_y] != self.grid[x][y]:
                break

            temp_coord[1] = [current_x, current_y]
            current_x -= 1
            current_y += 1
            number_align += 1

        if number_align >= 4:
            self.set_winner(self.grid[x][y])
            self.win_tokens_coord = temp_coord
            return True
        else:
            for x in range(0, self.grid_width):
                if self.grid[x][0] == TokenState.Blank:
                    return False

            self.game_win = True
            return False

    def test_win(self):
        """
        Test if there is a winner
        :return: Blank if nobody has won, Player_x: the player x has won
        """

        if self.is_win():
            return self.winner

        for x in range(0, self.grid_width):
            for y in range(0, self.grid_height):
                if self.grid[x][y] != TokenState.Blank and self.update_win(x, y):
                    return self.winner

        return TokenState.Blank  # draw

    def start_in_console(self):
        """
        Start a game in console
        :return: None
        """

        while True:
            print(str(self))
            while True:
                message = input("Choice a column (1 - 7): ")
                try:
                    message = int(message)
                except ValueError:
                    print("You must write a number between 1 and 7")
                    continue

                if message < 1 or 7 < message:
                    print("You must write a number between 1 and 7")
                    continue

                if self.add_token(message - 1)[0]:
                    if self.is_win():
                        print("Done.")
                        print("\n" * 2)
                        print(str(self))
                        return
                    print("Done.")
                    print(str(self))
                else:
                    print("You can't choose this column")

    def __str__(self):
        """
        Return grid status
        :return: string which contain a status to print
        """
        string = "Grid: \n"

        string += " | ".join((["{:^8}"] * self.grid_width)).format(*(range(1, self.grid_width + 1)))
        string += '\n'
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                string += "{:^8}".format(self.grid[x][y].name)
                string += (" | ", "\n")[x == self.grid_width - 1]  # if is the last element

        if self.is_win():
            string += "\033[92mThe winner is: {}\033[0m".format(self.winner.name)
        else:
            string += "\nIt's the turn of: " + self.current_turn.name

        return string

    def is_win(self):
        """
        If the power 4 is terminate / if anybody won
        :return: if anybody won (boolean)
        """

        return self.game_win

    def reset(self):
        """
        Reset the game
        :return: None
        """
        for x in range(0, self.grid_width):
            for y in range(0, self.grid_height):
                self.grid[x][y] = TokenState.Blank

        random.seed = int(time.time())
        self.current_turn = random.choice((TokenState.Player_1, TokenState.Player_2))

        self.game_win = False
        self.winner = TokenState.Blank
        self.win_tokens_coord = [[-1, -1], [-1, -1]]

    def set_winner(self, winner):
        """
        Set the winner
        :param winner: the winner
        :return: None
        """
        if not self.game_win:
            self.game_win = True
            self.winner = winner

            if winner == TokenState.Player_1:
                self.score[0] += 1
            elif winner == TokenState.Player_2:
                self.score[1] += 1

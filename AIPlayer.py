import copy
import random

import math

from TokenState import TokenState


def can_place_token(grid, column):
    """
    Return if you can place a token in the column
    :param grid: The grid
    :param column: The column to check
    :return: Boolean if you can
    """

    return grid[column][0] == TokenState.Blank


class AIPlayer(object):
    """
    A ai player
    """

    def __init__(self, min_max_deep, game):
        """
        Constructor
        :param min_max_deep: the deep
        :param game: link to game
        """
        self.min_max_deep = min_max_deep
        self.game = game
        self.thinking = False

    def run_turn(self):
        """
        Run his turn
        :return: the column to do
        """
        self.thinking = True

        score = -math.inf
        column_max_score = 0

        for column in range(0, self.game.grid_width):
            if can_place_token(self.game.grid, column):

                # print("Column: " + str(column))

                y_coord_new_token = self.get_coord_add_token_grid(self.game.grid, column)
                current_grid = copy.deepcopy(self.game.grid)
                current_grid[column][y_coord_new_token] = TokenState.Player_2

                align = [
                    self.get_number_horizontally_tokens(current_grid, column, y_coord_new_token),
                    self.get_number_vertically_tokens(current_grid, column, y_coord_new_token),
                    self.get_number_diagonal_bottom_left_tokens(current_grid, column, y_coord_new_token),
                    self.get_number_diagonal_top_left_tokens(current_grid, column, y_coord_new_token)
                ]  # list of all alignment of the new token

                # print(align)

                if align[0][0] >= 4 or align[1][0] >= 4 or align[2][0] >= 4 or align[3][0] >= 4:
                    column_max_score = column
                    break

                current_score = 0

                for i in range(0, 4):
                    if align[i][0] + align[i][1][0] + align[i][1][1] >= 4:
                        if align[i][0] == 3:
                            current_score += 14
                        
                        elif align[i][0] == 2:
                            current_score += 5
                            
                        elif align[i][0] == 1:
                            current_score += 2

                        # if align[i][0] > 1 and align[i][1][0] != 0 and align[i][1][1] != 0:
                        #     current_score += 1

                current_score += self.get_turn_min_max(current_grid, self.min_max_deep, TokenState.Player_1)
                # print(current_score)

                if current_score > score:
                    score = max(current_score, score)
                    column_max_score = column

                elif current_score == score:
                    if random.randint(0, 1) == 0:
                        score = max(current_score, score)
                        column_max_score = column

        self.thinking = False
        return column_max_score

    def get_turn_min_max(self, grid, deep, player_turn):
        """
        Recursive method to get turn min max
        :param grid: the current grid
        :param deep: the current deep
        :param player_turn: the player
        :return: current_score
        """

        if deep <= 0:
            raise RuntimeError("Error, you can't call with deep = 0")

        score = (math.inf, -math.inf)[player_turn == TokenState.Player_2]

        for column in range(0, self.game.grid_width):
            if can_place_token(grid, column):

                y_coord_new_token = self.get_coord_add_token_grid(grid, column)
                current_grid = copy.deepcopy(grid)
                current_grid[column][y_coord_new_token] = player_turn

                align = [
                    self.get_number_horizontally_tokens(current_grid, column, y_coord_new_token),
                    self.get_number_vertically_tokens(current_grid, column, y_coord_new_token),
                    self.get_number_diagonal_bottom_left_tokens(current_grid, column, y_coord_new_token),
                    self.get_number_diagonal_top_left_tokens(current_grid, column, y_coord_new_token)
                ]  # list of all alignment of the new token

                if player_turn == TokenState.Player_2:  # his turn
                    current_score = 0

                    if align[0][0] >= 4 or align[1][0] >= 4 or align[2][0] >= 4 or align[3][0] >= 4:
                        score = math.inf
                        break
                    else:
                        for i in range(0, 4):
                            if align[i][0] + align[i][1][0] + align[i][1][1] >= 4:
                                if align[i][0] == 3:
                                    current_score += 14

                                elif align[i][0] == 2:
                                    current_score += 5

                                elif align[i][0] == 1:
                                    current_score += 2

                                # if align[i][0] > 1 and align[i][1][0] != 0 and align[i][1][1] != 0:
                                #     current_score += 1

                        if deep > 1:
                            current_score += self.get_turn_min_max(
                                current_grid, deep - 1,
                                (TokenState.Player_1, TokenState.Player_2)[player_turn == TokenState.Player_1])

                    score = max(current_score, score)

                else:
                    current_score = 0
                    if align[0][0] >= 4 or align[1][0] >= 4 or align[2][0] >= 4 or align[3][0] >= 4:
                        score = -math.inf
                        break

                    else:

                        for i in range(0, 4):
                            if align[i][0] + align[i][1][0] + align[i][1][1] >= 4:
                                if align[i][0] == 3:
                                    current_score += -14

                                elif align[i][0] == 2:
                                    current_score += -5

                                elif align[i][0] == 1:
                                    current_score += -2

                                # if align[i][0] > 1 and align[i][1][0] != 0 and align[i][1][1] != 0:
                                #     current_score += -1

                        if deep > 1:
                            current_score += self.get_turn_min_max(
                                current_grid, deep - 1,
                                (TokenState.Player_1, TokenState.Player_2)[player_turn == TokenState.Player_1])

                    score = min(current_score, score)
        return score

    def get_coord_add_token_grid(self, grid, column):
        """
        Get the y coord of the token if you place a token in the column
        :param grid: The grid
        :param column: The column to which he add a token
        :return: y coord
        """

        for y in range(self.game.grid_height - 1, 0 - 1, -1):
            if grid[column][y] == TokenState.Blank:
                return y

    def get_number_horizontally_tokens(self, grid, x, y):
        """
        Get numbers of tokens horizontally
        :param grid: The grid
        :param x: the x to check
        :param y: the y to check
        :return: (number tokens align, (number blank align 1 side, 2 side))
        """

        if grid[x][y] == TokenState.Player_2:
            opponent_player = TokenState.Player_1
        elif grid[x][y] == TokenState.Player_1:
            opponent_player = TokenState.Player_2
        else:
            raise RuntimeError("You can't write coord which his token is Blank")

        number_align = 1
        number_blank_align = [0, 0]
        count_blank = False

        # right
        for current_x in range(x + 1, self.game.grid_width):
            if grid[current_x][y] == opponent_player:
                break
            elif count_blank:
                if grid[current_x][y] != TokenState.Blank:
                    break

                number_blank_align[0] += 1

            else:
                if grid[current_x][y] == TokenState.Blank:
                    count_blank = True
                else:
                    number_align += 1

        count_blank = False

        # left

        for current_x in range(x - 1, -1, -1):
            if grid[current_x][y] == opponent_player:
                break
            elif count_blank:
                if grid[current_x][y] != TokenState.Blank:
                    break

                number_blank_align[1] += 1

            else:
                if grid[current_x][y] == TokenState.Blank:
                    count_blank = True
                else:
                    number_align += 1

        return number_align, number_blank_align

    def get_number_vertically_tokens(self, grid, x, y):
        """
        Get numbers of tokens vertically
        :param grid: The grid
        :param x: the x to check
        :param y: the y to check
        :return: (number tokens align, (number blank align 1 side, 2 side))
        """

        if grid[x][y] == TokenState.Player_2:
            opponent_player = TokenState.Player_1
        elif grid[x][y] == TokenState.Player_1:
            opponent_player = TokenState.Player_2
        else:
            raise RuntimeError("You can't write coord which his token is Blank")

        number_align = 1
        number_blank_align = [0, 0]
        count_blank = False

        # bottom
        for current_y in range(y + 1, self.game.grid_height):
            if grid[x][current_y] == opponent_player:
                break
            elif count_blank:
                if grid[x][current_y] != TokenState.Blank:
                    break

                number_blank_align[0] += 1

            else:
                if grid[x][current_y] == TokenState.Blank:
                    count_blank = True
                else:
                    number_align += 1

        count_blank = False

        # top

        for current_y in range(y - 1, -1, -1):
            if grid[x][current_y] == opponent_player:
                break
            elif count_blank:
                if grid[x][current_y] != TokenState.Blank:
                    break

                number_blank_align[1] += 1

            else:
                if grid[x][current_y] == TokenState.Blank:
                    count_blank = True
                else:
                    number_align += 1

        return number_align, number_blank_align

    def get_number_diagonal_top_left_tokens(self, grid, x, y):
        """
        Get numbers of tokens align in diagonal top left
        :param grid: The grid
        :param x: the x to check
        :param y: the y to check
        :return: (number tokens align, (number blank align 1 side, 2 side))
        """

        if grid[x][y] == TokenState.Player_2:
            opponent_player = TokenState.Player_1
        elif grid[x][y] == TokenState.Player_1:
            opponent_player = TokenState.Player_2
        else:
            raise RuntimeError("You can't write coord which his token is Blank")

        number_align = 1
        number_blank_align = [0, 0]
        count_blank = False

        current_x = x + 1
        current_y = y + 1

        # right
        while current_x < self.game.grid_width and current_y < self.game.grid_height:
            if grid[current_x][current_y] == opponent_player:
                break
            elif count_blank:
                if grid[current_x][current_y] != TokenState.Blank:
                    break

                number_blank_align[0] += 1

            else:
                if grid[current_x][current_y] == TokenState.Blank:
                    count_blank = True
                else:
                    number_align += 1

            current_x += 1
            current_y += 1

        current_x = x - 1
        current_y = y - 1
        count_blank = False

        # left

        while current_x >= 0 and current_y >= 0:
            if grid[current_x][current_y] == opponent_player:
                break
            elif count_blank:
                if grid[current_x][current_y] != TokenState.Blank:
                    break

                number_blank_align[1] += 1

            else:
                if grid[current_x][current_y] == TokenState.Blank:
                    count_blank = True
                else:
                    number_align += 1

            current_x -= 1
            current_y -= 1

        return number_align, number_blank_align

    def get_number_diagonal_bottom_left_tokens(self, grid, x, y):
        """
        Get numbers of tokens align in diagonal bottom left
        :param grid: The grid
        :param x: the x to check
        :param y: the y to check
        :return: (number tokens align, (number blank align 1 side, 2 side))
        """

        if grid[x][y] == TokenState.Player_2:
            opponent_player = TokenState.Player_1
        elif grid[x][y] == TokenState.Player_1:
            opponent_player = TokenState.Player_2
        else:
            raise RuntimeError("You can't write coord which his token is Blank")

        number_align = 1
        number_blank_align = [0, 0]
        count_blank = False

        current_x = x + 1
        current_y = y - 1

        # right
        while current_x < self.game.grid_width and current_y >= 0:
            if grid[current_x][current_y] == opponent_player:
                break
            elif count_blank:
                if grid[current_x][current_y] != TokenState.Blank:
                    break

                number_blank_align[0] += 1

            else:
                if grid[current_x][current_y] == TokenState.Blank:
                    count_blank = True
                else:
                    number_align += 1

            current_x += 1
            current_y -= 1

        current_x = x - 1
        current_y = y + 1
        count_blank = False

        # left

        while current_x >= 0 and current_y < self.game.grid_height:
            if grid[current_x][current_y] == opponent_player:
                break
            elif count_blank:
                if grid[current_x][current_y] != TokenState.Blank:
                    break

                number_blank_align[1] += 1

            else:
                if grid[current_x][current_y] == TokenState.Blank:
                    count_blank = True
                else:
                    number_align += 1

            current_x -= 1
            current_y += 1

        return number_align, number_blank_align

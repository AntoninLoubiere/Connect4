import copy
import random

import math

from main import Player
from main.TokenState import TokenState

POSITION_EVALUATION_TABLE = [
    [3, 4, 5, 7, 5, 4, 3],
    [4, 6, 8, 10, 8, 6, 4],
    [5, 8, 11, 13, 11, 8, 5],
    [5, 8, 11, 13, 11, 8, 5],
    [4, 6, 8, 10, 8, 6, 4],
    [3, 4, 5, 7, 5, 4, 3]
]
ALIGNMENT_COEFFICIENT = [0, 10, 100, 1000000000000000]
MAX_SCORE = 1000000000000000
MIN_SCORE = -1000000000000000


def can_place_token(grid, column):
    """
    Return if you can place a token in the column
    :param grid: The grid
    :param column: The column to check
    :return: Boolean if you can
    """

    return grid[column][0] == TokenState.Blank


class AIPlayer(Player.Player):
    """
    A ai player
    """

    def __init__(self, min_max_deep, game, player_enum, token, name=None):
        """
        Constructor
        :param min_max_deep: the deep
        :param game: link to game
        """
        super().__init__(player_enum, token, name)

        if name is None:
            self.name = ("Computer 2", "Computer 1")[self.player_enum == TokenState.Player_1]
        else:
            self.name = name

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
        column_max_score_possibility = []

        print(self.get_evaluation(self.game.grid))

        for column in range(0, self.game.grid_width):
            if can_place_token(self.game.grid, column):

                print("Column: " + str(column))

                y_coord_new_token = self.get_coord_add_token_grid(self.game.grid, column)
                current_grid = copy.deepcopy(self.game.grid)
                current_grid[column][y_coord_new_token] = self.player_enum

                align = [
                    self.get_alignment_two_side(current_grid, column, y_coord_new_token, 0, 1),
                    self.get_alignment_two_side(current_grid, column, y_coord_new_token, 1, 0),
                    self.get_alignment_two_side(current_grid, column, y_coord_new_token, 1, 1),
                    self.get_alignment_two_side(current_grid, column, y_coord_new_token, 1, -1)
                ]  # list of all alignment of the new token

                # print(align)

                if align[0][0] >= 4 or align[1][0] >= 4 or align[2][0] >= 4 or align[3][0] >= 4:
                    column_max_score_possibility = [column]
                    break

                current_score = self.get_turn_min_max(current_grid, self.min_max_deep,
                                                      (TokenState.Player_1, TokenState.Player_2)[
                                                          self.player_enum == TokenState.Player_1],
                                                      +math.inf, -math.inf)
                # print(current_score)
                print("Score choose:", current_score)

                if current_score > score:
                    score = max(current_score, score)
                    column_max_score_possibility = [column]

                elif current_score == score:
                    score = max(current_score, score)
                    column_max_score_possibility.append(column)

        self.thinking = False
        if len(column_max_score_possibility) == 0:
            return 0
        else:
            return random.choice(column_max_score_possibility)

    def get_turn_min_max(self, grid, deep, player_turn, alpha, beta):
        """
        Recursive method to get turn min max
        :param alpha: The alpha of the algorithm. alpha > beta
        :param beta: The beta of the algorithm. beta < alpha
        :param grid: the current grid
        :param deep: the current deep
        :param player_turn: the player
        :return: current_score
        """
        if deep <= 0:
            raise RuntimeError("Error, you can't call with deep = 0")

        score = (math.inf, -math.inf)[player_turn == self.player_enum]

        for column in range(0, self.game.grid_width):
            if can_place_token(grid, column):

                y_coord_new_token = self.get_coord_add_token_grid(grid, column)
                current_grid = copy.deepcopy(grid)
                current_grid[column][y_coord_new_token] = player_turn

                align = [
                    self.get_alignment_two_side(current_grid, column, y_coord_new_token, 0, 1),
                    self.get_alignment_two_side(current_grid, column, y_coord_new_token, 1, 0),
                    self.get_alignment_two_side(current_grid, column, y_coord_new_token, 1, 1),
                    self.get_alignment_two_side(current_grid, column, y_coord_new_token, 1, -1)
                ]  # list of all alignment of the new token

                # print(align)

                if player_turn == self.player_enum:  # his turn
                    if align[0][0] >= 4 or align[1][0] >= 4 or align[2][0] >= 4 or align[3][0] >= 4:
                        return 1000000000000000000 - (self.min_max_deep - deep)

                    elif deep > 1:
                        current_score = self.get_turn_min_max(
                            current_grid, deep - 1,
                            (TokenState.Player_1, TokenState.Player_2)[player_turn == TokenState.Player_1], alpha,
                            beta)

                    else:
                        current_score = self.get_evaluation(current_grid)

                    score = max(current_score, score)

                    if alpha <= score:  # alpha cut
                        return score
                    beta = max(beta, score)

                else:
                    if align[0][0] >= 4 or align[1][0] >= 4 or align[2][0] >= 4 or align[3][0] >= 4:
                        return -1000000000000000000 + (self.min_max_deep - deep)

                    elif deep > 1:
                        current_score = self.get_turn_min_max(
                            current_grid, deep - 1,
                            (TokenState.Player_1, TokenState.Player_2)[player_turn == TokenState.Player_1], alpha,
                            beta)

                    else:
                        current_score = self.get_evaluation(current_grid)

                    if deep == self.min_max_deep:
                        print(current_score)

                    score = min(current_score, score)
                    if beta >= score:  # beta cut
                        return score
                    alpha = min(alpha, score)

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

    def get_evaluation(self, grid):
        """
        Get the evaluation of the grid
        :param grid: the grid
        :return: The score of the grid
        """
        score = 0
        opponent = TokenState.get_opponent(self.player_enum)

        visited = []
        for x in range(0, self.game.grid_width):
            visited.append([])
            for y in range(0, self.game.grid_height):
                visited[x].append(False)

        for x in range(0, self.game.grid_width):
            for y in range(0, self.game.grid_height):
                # alignment evaluation table
                if grid[x][y] != TokenState.Blank:
                    if not visited[x][y]:
                        alignments = [
                            self.get_alignment_two_side(grid, x, y, 1, 0, visited),
                            self.get_alignment_two_side(grid, x, y, 0, 1, visited),
                            self.get_alignment_two_side(grid, x, y, 1, 1, visited),
                            self.get_alignment_two_side(grid, x, y, 1, -1, visited),
                        ]
                        # self.print_grid(grid, x, y)
                        # print(alignments)
                        for alignment in alignments:
                            if alignment[1] >= 4:
                                align_number = alignment[0]
                                if alignment[0] > len(ALIGNMENT_COEFFICIENT):
                                    align_number = len(ALIGNMENT_COEFFICIENT)
                                if grid[x][y] == self.player_enum:
                                    score += ALIGNMENT_COEFFICIENT[align_number - 1]
                                else:
                                    score -= ALIGNMENT_COEFFICIENT[align_number - 1]

                    # position evaluation point
                    if grid[x][y] == self.player_enum:
                        score += POSITION_EVALUATION_TABLE[y][x]
                    elif grid[x][y] == opponent:
                        score -= POSITION_EVALUATION_TABLE[y][x]

        return max(min(score, MAX_SCORE), MIN_SCORE)

    def get_alignment_two_side(self, grid, x, y, x_offset, y_offset, visited=None):
        """
        Get the number of token in the same line
        :param visited: The list of visited token
        :param grid: The grid to scan
        :param x: the x coord of the token
        :param y:the y coord of the token
        :param x_offset: the x_offset to scan
        :param y_offset: the y offset to scan
        :return: number token align, number alignment max possible
        """
        alignment1 = self.get_alignment_one_side(grid, x, y, x_offset, y_offset, visited)
        alignment2 = self.get_alignment_one_side(grid, x, y, x_offset * -1, y_offset * -1, visited)
        # print(x, y, x_offset, y_offset, alignment1, alignment2)
        return alignment1[0] + alignment2[0] - 1, alignment1[1] + alignment2[1] - 1  # It count the tile x, y twice

    def get_alignment_one_side(self, grid, x, y, x_offset, y_offset, visited=None):
        """
        Get the number of token in the same line ONE SIDE
        :param visited: The list of visited token
        :param grid: The grid to scan
        :param x: the x coord of the token
        :param y:the y coord of the token
        :param x_offset: the x_offset to scan
        :param y_offset: the y offset to scan
        :return: number token align, number alignment max possible
        """
        blank_mode = False
        number_align = 1
        number_align_blank = 1
        blank_space = 0
        current_x = x + x_offset
        current_y = y + y_offset

        while self.valid_position(current_x, current_y):
            if blank_mode:
                if grid[current_x][current_y] == self.player_enum:
                    if blank_space < 1 and number_align < 3:  # set max to 3
                        number_align_blank += 1
                        blank_space += 1
                        number_align += 1
                    else:
                        break
                if grid[current_x][current_y] == TokenState.Blank:
                    number_align_blank += 1
                    blank_space += 1
                else:
                    # if is the opponent
                    break

            elif grid[current_x][current_y] == grid[x][y]:
                number_align += 1
                number_align_blank += 1

                if visited is not None:
                    visited[current_x][current_y] = True

            elif grid[current_x][current_y] == TokenState.Blank:
                blank_mode = True
                blank_space = 0
                number_align_blank += 1
            else:
                break

            current_x += x_offset
            current_y += y_offset

        return number_align, number_align_blank

    def valid_position(self, x, y):
        """
        Test if the position x, y is valid
        :param x: the x coord of the token
        :param y: the y coord of the token
        :return: boolean if is possible
        """
        return 0 <= x < self.game.grid_width and 0 <= y < self.game.grid_height

    def get_thinking(self):
        """
        Get if is thinking
        :return: None
        """
        return self.thinking

    def print_grid(self, grid, x, y):
        print("X: " + str(x) + " Y: " + str(y))
        for y in range(0, self.game.grid_height):
            for x in range(0, self.game.grid_width):
                print('{:7}|'.format(grid[x][y].name), end='')
            print("")

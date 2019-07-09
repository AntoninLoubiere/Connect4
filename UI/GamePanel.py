from UI import Panel, ImageGetter, TokenColor
import TokenState
import tkinter.tix
import Game
from UI.ResizingCanvas import ResizingCanvas


class GamePanel(Panel.Panel):
    """
    GamePanel is a panel for UI, is the UI for the game
    """

    def __init__(self, master, ui, **kwargs):
        """
        Constructor
        :param master: see Panel class
        :param ui: see Panel class
        """
        super().__init__(master, ui)

        self.turn_text_format = "It's the turn of: {}"
        self.win_text_format = "The winner is: {}"

        self.grid_canvas = ResizingCanvas(self, self.ui, self.draw_grid)
        self.grid_canvas.pack(expand=True, fill=tkinter.tix.BOTH)
        self.grid_canvas.bind("<Button>", self.grid_canvas_on_click)

        self.game = Game.Game(**kwargs)

        self.token_square_size = 0

        self.height_center = 0
        self.width_center = 0
        self.turn_text_height = 10

        self.image_getter = ImageGetter.ImageGetter(token_size=self.token_square_size)

        self.player_token_color = {
            TokenState.TokenState.Player_1: TokenColor.TokenColor.Blue,
            TokenState.TokenState.Player_2: TokenColor.TokenColor.Red
        }

        self.grid_image_create = []
        self.turn_text_id = -1

        for x in range(0, self.game.grid_width):
            self.grid_image_create.append([])
            for y in range(0, self.game.grid_height):
                self.grid_image_create[x].append(0)

        self.draw_grid()

    def draw_grid(self):
        """
        Draw the grid in the canvas
        :return: None
        """

        space_between_column_line = (self.grid_canvas.width - 10) / float(self.game.grid_width)
        space_between_row_line = (self.grid_canvas.height - 20 - self.turn_text_height) / float(self.game.grid_height)
        self.token_square_size = min(space_between_column_line, space_between_row_line)

        #  print(space_between_column_line, space_between_column_line, self.token_square_size)

        self.height_center = (self.grid_canvas.height - self.token_square_size * self.game.grid_height) / 2.
        self.width_center = (self.grid_canvas.width - self.token_square_size * self.game.grid_width) / 2.

        self.grid_canvas.delete("grid")

        self.turn_text_id = self.grid_canvas.create_text(self.grid_canvas.width / 2, self.turn_text_height, tag="grid")
        self.update_turn_label()

        self.grid_canvas.create_rectangle(self.width_center, self.height_center + self.turn_text_height,
                                          self.grid_canvas.width - self.width_center,
                                          self.grid_canvas.height - self.height_center + self.turn_text_height,
                                          tag="grid", fill="#DDD")

        for i in range(1, self.game.grid_width):
            self.grid_canvas.create_line(self.token_square_size * i + self.width_center,
                                         self.height_center + self.turn_text_height,
                                         self.token_square_size * i + self.width_center,
                                         self.grid_canvas.height - self.height_center + self.turn_text_height,
                                         tag="grid")

        for i in range(1, self.game.grid_height):
            self.grid_canvas.create_line(self.width_center,
                                         self.token_square_size * i + self.height_center + self.turn_text_height,
                                         self.grid_canvas.width - self.width_center,
                                         self.token_square_size * i + self.height_center + self.turn_text_height,
                                         tag="grid")

        self.recreate_images()

    def recreate_images(self):
        """
        Recreate images when the canvas is resize
        :return: None
        """

        self.image_getter.resize_tokens_images(self.token_square_size)

        for x in range(0, self.game.grid_width):
            for y in range(0, self.game.grid_height):
                if self.grid_image_create[x][y] != 0:
                    self.grid_canvas.delete(self.grid_image_create[x][y])

                if self.game.grid[x][y] != TokenState.TokenState.Blank:
                    self.create_image(x, y, self.game.grid[x][y])

    def create_image(self, x, y, player):
        """
        Create a image at the 
        :param player: the player which place the token
        :param x: the x coord of the image
        :param y: the y coord of the image
        :return: None
        """

        coord = self.get_square_coord(x, y)

        if self.grid_image_create[x][y] != 0:
            self.grid_canvas.delete(self.grid_image_create[x][y])
            # noinspection PyTypeChecker
            self.grid_image_create[x][y] = 0

        self.grid_image_create[x][y] = self.grid_canvas.create_image(
            coord[0][0], coord[0][1], image=self.image_getter.save_photos[player][self.player_token_color[player]],
            anchor=tkinter.tix.NW
        )

    def grid_canvas_on_click(self, event):
        """
        When the canvas is click
        :param event: the event
        :return: None
        """
        if event.num == 1:
            column = (event.x - self.width_center) / self.token_square_size
            if 0 <= column <= self.game.grid_width:
                self.add_token_column(int(column))

    def add_token_column(self, column):
        """
        Add a token in the column
        :param column: the column
        :return: None
        """

        current_player = self.game.current_turn

        add_token_result = self.game.add_token(column)

        if add_token_result[0]:
            self.create_image(add_token_result[1][0], add_token_result[1][1], current_player)
            self.update_turn_label()

    def get_square_coord(self, x, y):
        """
        Get the coord of a square
        :return: A list of lists with coordinates, 0: top left, 1: bottom right; x: 0, y:1
        """

        return [
            [
                x * self.token_square_size + self.width_center,
                y * self.token_square_size + self.height_center + self.turn_text_height
            ],
            [
                (x + 1) * self.token_square_size + self.width_center,
                (y + 1) * self.token_square_size + self.height_center + self.turn_text_height
            ]
        ]

    def update_turn_label(self):
        """
        Update the turn label
        :return: None
        """
        if self.game.is_win():
            self.grid_canvas.itemconfigure(self.turn_text_id, text=self.win_text_format.format(
                ("Player 2", "Player 1")[self.game.winner == TokenState.TokenState.Player_1]), fill="green")
        else:
            self.grid_canvas.itemconfigure(self.turn_text_id, text=self.turn_text_format.format(
                ("Player 2", "Player 1")[self.game.current_turn == TokenState.TokenState.Player_1]))

from UI import Panel, ImageGetter, TokenColor
import TokenState
import tkinter.tix
import Game


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

        self.grid_canvas = tkinter.tix.Canvas(self, width=600, height=400)
        self.grid_canvas.grid(row=1, column=0)
        self.grid_canvas.bind("<Button>", self.grid_canvas_on_click)

        self.game = Game.Game(**kwargs)

        space_between_column_line = self.grid_canvas.winfo_reqwidth() / float(self.game.grid_width)
        space_between_row_line = self.grid_canvas.winfo_reqheight() / float(self.game.grid_height)
        self.token_square_size = min(space_between_column_line, space_between_row_line)

        self.height_center = (self.grid_canvas.winfo_reqheight() - self.token_square_size * self.game.grid_height) / 2
        self.width_center = (self.grid_canvas.winfo_reqwidth() - self.token_square_size * self.game.grid_width) / 2

        self.image_getter = ImageGetter.ImageGetter(token_size=self.token_square_size)

        self.player_token_color = {
            TokenState.TokenState.Player_1: TokenColor.TokenColor.Blue,
            TokenState.TokenState.Player_2: TokenColor.TokenColor.Green
        }

        self.grid_image_create = []

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

        for i in range(0, self.game.grid_width + 1):
            self.grid_canvas.create_line(self.token_square_size * i + self.width_center, self.height_center,
                                         self.token_square_size * i + self.width_center,
                                         self.grid_canvas.winfo_reqheight() - self.height_center, tag="grid")

        for i in range(0, self.game.grid_height + 1):
            self.grid_canvas.create_line(self.width_center, self.token_square_size * i + self.height_center,
                                         self.grid_canvas.winfo_reqwidth() - self.width_center,
                                         self.token_square_size * i + self.height_center)
            
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

        print(add_token_result)

        if add_token_result[0]:
            self.create_image(add_token_result[1][0], add_token_result[1][1], current_player)

    def get_square_coord(self, x, y):
        """
        Get the coord of a square
        :return: A list of lists with coordinates, 0: top left, 1: bottom right; x: 0, y:1
        """

        return [
            [
                x * self.token_square_size + self.width_center,
                y * self.token_square_size + self.height_center
            ],
            [
                (x + 1) * self.token_square_size + self.width_center,
                (y + 1) * self.token_square_size + self.height_center
            ]
        ]

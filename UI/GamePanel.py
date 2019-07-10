from UI import Panel, ImageGetter, TokenColor, TokenFallAnimation
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

        self.grid_canvas = ResizingCanvas(self, self.ui, self.on_resize)
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
            TokenState.TokenState.Player_2: TokenColor.TokenColor.Orange
        }

        self.grid_image_create = []
        self.turn_text_id = -1
        self.win_line_id = -1

        for x in range(0, self.game.grid_width):
            self.grid_image_create.append([])
            for y in range(0, self.game.grid_height):
                self.grid_image_create[x].append(-1)

        self.token_animation_list = []

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
                if self.grid_image_create[x][y] != -1:
                    self.grid_canvas.delete(self.grid_image_create[x][y])
                    self.create_image(x, y, self.game.grid[x][y])

    def on_resize(self):
        """
        When the grid is resize
        :return: None
        """
        self.draw_grid()

        if self.game.is_win():
            self.draw_win_line()

    def redraw_animation(self):
        """
        Redraw animation
        :return: None
        """
        if len(self.token_animation_list) > 0:
            token_animation_to_remove = list(self.token_animation_list)

            print(token_animation_to_remove)

            i = 0

            while i > len(token_animation_to_remove):
                print(token_animation_to_remove[i])
                animation_to_add = TokenFallAnimation.TokenFallAnimation(
                    token_animation_to_remove[i].final_x, token_animation_to_remove[i].final_y,
                    token_animation_to_remove[i].player, self)

                animation_to_add.set_current_height(token_animation_to_remove[i].current_height)

                self.add_token_animation(animation_to_add)
                print(animation_to_add)

                self.remove_token_animation(token_animation_to_remove[i])
                
                i += 1

    def create_image(self, x, y, player):
        """
        Create a image at the 
        :param player: the player which place the token
        :param x: the x coord of the image
        :param y: the y coord of the image
        :return: None
        """

        coord = self.get_square_coord(x, y)

        if self.grid_image_create[x][y] != -1:
            self.grid_canvas.delete(self.grid_image_create[x][y])
            # noinspection PyTypeChecker
            self.grid_image_create[x][y] = 0

        self.grid_image_create[x][y] = self.grid_canvas.create_image(
            coord[0][0], coord[0][1], image=self.image_getter.save_photos[player][self.player_token_color[player]],
            anchor=tkinter.tix.NW
        )

        if self.game.is_win():
            self.draw_win_line()

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
            self.add_token_animation(TokenFallAnimation.TokenFallAnimation(
                add_token_result[1][0], add_token_result[1][1], current_player, self))
            self.update_turn_label()
            if self.game.is_win():
                self.on_win()

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

    def on_win(self):
        """
        When a player win
        :return: None
        """
        self.grid_canvas.unbind("<Button>")
        self.draw_win_line()

    def all_win_tokens_are_fall(self):
        """
        Test if all tokens are fall
        :return: If there are fall
        """
        x_speed = 0
        y_speed = 0

        if self.game.win_tokens_coord[0][0] < self.game.win_tokens_coord[1][0]:
            x_speed = 1
        elif self.game.win_tokens_coord[0][0] > self.game.win_tokens_coord[1][0]:
            x_speed = -1

        if self.game.win_tokens_coord[0][1] < self.game.win_tokens_coord[1][1]:
            y_speed = 1
        elif self.game.win_tokens_coord[0][1] > self.game.win_tokens_coord[1][1]:
            y_speed = -1

        current_x = self.game.win_tokens_coord[0][0]
        current_y = self.game.win_tokens_coord[0][1]

        while current_x != self.game.win_tokens_coord[1][0] + x_speed or \
                current_y != self.game.win_tokens_coord[1][1] + y_speed:
            if self.grid_image_create[current_x][current_y] == -1:  # They aren't images
                return False

            current_x += x_speed
            current_y += y_speed

        return True

    def draw_win_line(self):
        """
        Draw the win line
        :return: None
        """

        if self.all_win_tokens_are_fall():
            coord_1 = self.get_square_coord(self.game.win_tokens_coord[0][0], self.game.win_tokens_coord[0][1])
            coord_1 = [coord_1[0][0] + (coord_1[1][0] - coord_1[0][0]) / 2.,
                       coord_1[0][1] + (coord_1[1][1] - coord_1[0][1]) / 2.]  # get coord in the center

            coord_2 = self.get_square_coord(self.game.win_tokens_coord[1][0], self.game.win_tokens_coord[1][1])
            coord_2 = [coord_2[0][0] + (coord_2[1][0] - coord_2[0][0]) / 2.,
                       coord_2[0][1] + (coord_2[1][1] - coord_2[0][1]) / 2.]  # get coord in the center

            if self.win_line_id != -1:
                self.grid_canvas.delete(self.win_line_id)
            self.win_line_id = self.grid_canvas.create_line(
                coord_1[0], coord_1[1], coord_2[0], coord_2[1], width=5, fill="green")

    def tick_update(self):
        """
        See panel class
        :return: See panel class
        """

        i = 0
        while i < len(self.token_animation_list):
            self.token_animation_list[i].tick_update()
            i += 1

    def add_token_animation(self, token_animation):
        """
        Add a token animation
        :param token_animation: The animation to add
        :return: None
        """
        self.token_animation_list.append(token_animation)

    def remove_token_animation(self, token_animation):
        """
        Remove a token animation
        :param token_animation: the token animation to remove
        :return: None
        """
        if self.token_animation_list.count(token_animation) >= 1:
            self.token_animation_list.remove(token_animation)
            token_animation.on_remove()
        else:
            i = 0
            while i < len(self.token_animation_list):
                if token_animation.id == self.token_animation_list[i].id:
                    self.token_animation_list.pop(i)
                    return None

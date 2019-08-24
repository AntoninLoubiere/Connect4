import threading
import time
import tkinter.tix

from UI import Panel, TokenStyle, TokenFallAnimation
from main import TokenState, Game, AIPlayer, Player, Preferences


class GamePanel(Panel.Panel):
    """
    GamePanel is a panel for UI, is the UI for the game
    """

    def __init__(self, master, ui,
                 player_1=Player.Player(TokenState.TokenState.Player_1, TokenStyle.TokenStyle.Blue),
                 player_2=Player.Player(TokenState.TokenState.Player_2, TokenStyle.TokenStyle.Green),
                 game=Game.Game(), disable_end_button=False, delay=Preferences.DEFAULT_DELAY):
        """
        Constructor
        :param player_1: the player 1
        :param player_2: the player 2
        :param game: a link to the game
        :param disable_end_button: if need to disable end buttons (for the client)
        :param delay: the delay between click in ms
        :param master: see Panel class
        :param ui: see Panel class
        """
        super().__init__(master, ui)

        self.turn_text_format = self.ui.translation.get_translation("game_panel_turn_format")
        self.win_text_format = self.ui.translation.get_translation("game_panel_win_format")

        self.grid_canvas = tkinter.tix.Canvas(self)
        self.grid_canvas.pack(expand=True, fill=tkinter.tix.BOTH)

        self.after(500, lambda: self.grid_canvas.bind("<Button>", self.grid_canvas_on_click))

        self.game = game

        self.players = {
            TokenState.TokenState.Player_1: player_1,
            TokenState.TokenState.Player_2: player_2
        }

        self.token_square_size = 0

        self.height_center = 0
        self.width_center = 0
        self.turn_text_height = 15

        self.button_main_menu = tkinter.tix.Button(
            self,
            # text=self.ui.translation.get_translation("game_panel_main_menu_button"),
            command=self.button_main_menu_command, image=self.ui.image_getter.door_exit_icon)
        self.button_main_menu.place(x=0, y=0)

        self.grid_image_create = []
        self.turn_text_id = -1
        self.turn_image_id = - 1
        self.win_line_id = -1
        self.win_icon_id = -1
        self.win_icon_background_id = -1

        self.win_text_frame = tkinter.tix.Frame(self, relief=tkinter.tix.RAISED, borderwidth=2)

        self.win_text_label = tkinter.tix.Label(self.win_text_frame)
        self.win_text_label.grid(row=0, column=0)

        if not disable_end_button:
            self.end_buttons_frame = tkinter.tix.Frame(self.win_text_frame)
            self.end_buttons_frame.columnconfigure(0, weight=1)
            self.end_buttons_frame.columnconfigure(1, weight=1)
            self.end_buttons_frame.grid(row=1, column=0)

            max_width = max(len(self.ui.translation.get_translation("back")),
                            len(self.ui.translation.get_translation("restart")),
                            len(self.ui.translation.get_translation("main_menu")))

            self.button_main_menu_end = tkinter.tix.Button(
                self.end_buttons_frame,
                text=self.ui.translation.get_translation("main_menu"),
                command=self.button_main_menu_command, width=max_width
            )
            self.button_main_menu_end.grid(row=0, column=0, sticky=tkinter.tix.NSEW, padx=5)

            self.back_button = tkinter.tix.Button(
                self.end_buttons_frame,
                text=self.ui.translation.get_translation("back"),
                command=self.button_back_command, width=max_width
            )
            self.back_button.grid(row=0, column=1, sticky=tkinter.tix.NSEW, padx=5)

            self.restart_button = tkinter.tix.Button(
                self.end_buttons_frame,
                text=self.ui.translation.get_translation("restart"),
                command=self.button_restart_command, width=max_width
            )
            self.restart_button.grid(row=0, column=2, sticky=tkinter.tix.NSEW, padx=5)

        for x in range(0, self.game.grid_width):
            self.grid_image_create.append([])
            for y in range(0, self.game.grid_height):
                self.grid_image_create[x].append(-1)

        self.token_animation_list = []

        self.delay = delay / 1000.  # convert in second
        self.last_click_time = time.time()

    def destroy(self):
        """
        When the panel is destroy, force the AI turn to stop
        :return: None
        """
        if isinstance(self.players[TokenState.TokenState.Player_1], AIPlayer.AIPlayer) and \
                self.players[TokenState.TokenState.Player_1].get_thinking():
            self.players[TokenState.TokenState.Player_1].stop_turn()

        if isinstance(self.players[TokenState.TokenState.Player_2], AIPlayer.AIPlayer) and \
                self.players[TokenState.TokenState.Player_2].get_thinking():
            self.players[TokenState.TokenState.Player_2].stop_turn()

        self.remove_all_token_animation()

        super().destroy()

    def on_create_finish(self):
        """
        See panel class
        :return: See panel class
        """
        self.on_resize(None)

        if isinstance(self.players[self.game.current_turn], AIPlayer.AIPlayer):
            thread = threading.Thread(target=self.run_ai_turn)
            thread.start()

    def draw_grid(self):
        """
        Draw the grid in the canvas
        :return: None
        """

        space_between_column_line = (self.grid_canvas.winfo_width() - 10) / float(self.game.grid_width)
        space_between_row_line = (self.grid_canvas.winfo_height() - 20 - self.turn_text_height
                                  ) / float(self.game.grid_height)
        self.token_square_size = min(space_between_column_line, space_between_row_line)

        #  print(space_between_column_line, space_between_column_line, self.token_square_size)

        self.height_center = (self.grid_canvas.winfo_height() - self.token_square_size * self.game.grid_height) / 2.
        self.width_center = (self.grid_canvas.winfo_width() - self.token_square_size * self.game.grid_width) / 2.

        self.grid_canvas.delete("grid")

        self.turn_text_id = self.grid_canvas.create_text(self.grid_canvas.winfo_width() / 2, self.turn_text_height,
                                                         tag="grid")

        self.grid_canvas.create_rectangle(self.width_center, self.height_center + self.turn_text_height,
                                          self.grid_canvas.winfo_width() - self.width_center,
                                          self.grid_canvas.winfo_height() - self.height_center +
                                          self.turn_text_height,
                                          tag="grid", fill="#DDD")

        for i in range(1, self.game.grid_width):
            self.grid_canvas.create_line(self.token_square_size * i + self.width_center,
                                         self.height_center + self.turn_text_height,
                                         self.token_square_size * i + self.width_center,
                                         self.grid_canvas.winfo_height() - self.height_center +
                                         self.turn_text_height,
                                         tag="grid")

        for i in range(1, self.game.grid_height):
            self.grid_canvas.create_line(self.width_center,
                                         self.token_square_size * i + self.height_center + self.turn_text_height,
                                         self.grid_canvas.winfo_width() - self.width_center,
                                         self.token_square_size * i + self.height_center + self.turn_text_height,
                                         tag="grid")

        self.recreate_images()
        self.update_turn_label()

    def recreate_images(self):
        """
        Recreate images when the canvas is resize
        :return: None
        """

        self.ui.image_getter.resize_tokens_images(self.token_square_size)

        for x in range(0, self.game.grid_width):
            for y in range(0, self.game.grid_height):
                if self.grid_image_create[x][y] != -1:
                    self.create_image(x, y, self.game.grid[x][y])

    def on_resize(self, event):
        """
        When the grid is resize
        :return: None
        """
        self.draw_grid()

        if self.game.is_win():
            self.update_win()

        super().on_resize(event)

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
            coord[0][0], coord[0][1],
            image=self.ui.image_getter.save_token_photos[player][self.players[player].token],
            anchor=tkinter.tix.NW
        )

    def grid_canvas_on_click(self, event):
        """
        When the canvas is click
        :param event: the event
        :return: None
        """
        if event.num == 1 and time.time() >= self.last_click_time + self.delay:
            column = (event.x - self.width_center) / self.token_square_size
            if 0 <= column <= self.game.grid_width:
                if not isinstance(self.players[self.game.current_turn], AIPlayer.AIPlayer):
                    self.last_click_time = time.time()
                    self.add_token_column(int(column))

    def add_token_column(self, column):
        """
        Add a token in the column
        :param column: the column
        :return: if is do
        """

        current_player = self.game.current_turn

        add_token_result = self.game.add_token(column)

        if add_token_result[0]:
            self.add_token_animation(TokenFallAnimation.TokenFallAnimation(
                add_token_result[1][0], add_token_result[1][1], current_player, self))
            self.update_turn_label()
            if self.game.is_win():
                self.on_win()
        return add_token_result

    def add_token_with_coord(self, x, y):
        """
        Add a token with coord
        :param y: the y cooed
        :param x: the x coord
        :return: if is do
        """
        current_player = self.game.current_turn

        add_token_result = self.game.add_token_with_coord(x, y)

        if add_token_result[0]:
            self.add_token_animation(TokenFallAnimation.TokenFallAnimation(
                add_token_result[1][0], add_token_result[1][1], current_player, self))
            self.update_turn_label()
            if self.game.is_win():
                self.on_win()
        return add_token_result

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

        if self.game.is_win() and self.game.winner != TokenState.TokenState.Blank:
            self.grid_canvas.itemconfigure(self.turn_text_id, text=self.win_text_format.format(
                self.players[self.game.winner].name), fill="green")

            if self.turn_image_id != -1:
                self.grid_canvas.delete(self.turn_image_id)

            self.turn_image_id = self.grid_canvas.create_image(
                self.grid_canvas.bbox(self.turn_text_id)[2] + 5, 0,
                image=self.ui.image_getter.save_token_icons
                [self.game.winner][self.players[self.game.winner].token],
                anchor=tkinter.tix.NW
            )

        elif self.game.is_win():
            self.grid_canvas.itemconfigure(
                self.turn_text_id,
                text=self.ui.translation.get_translation("draw"), fill="green")
            if self.turn_image_id != -1:
                self.grid_canvas.delete(self.turn_image_id)

        else:
            self.grid_canvas.itemconfigure(self.turn_text_id, text=self.turn_text_format.format(
                self.players[self.game.current_turn].name))

            if self.turn_image_id != -1:
                self.grid_canvas.delete(self.turn_image_id)

            self.turn_image_id = self.grid_canvas.create_image(
                self.grid_canvas.bbox(self.turn_text_id)[2] + 5, 0,
                image=self.ui.image_getter.save_token_icons
                [self.game.current_turn][self.players[self.game.current_turn].token],
                anchor=tkinter.tix.NW
            )

    def on_win(self):
        """
        When a player win
        :return: None
        """
        self.grid_canvas.unbind("<Button>")
        self.update_win()

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

    def all_tokens_are_fall(self):
        """
        Test if all tokens are fall
        :return: boolean if all token are fall
        """
        for x in range(0, self.game.grid_width):
            if self.grid_image_create[x][0] == -1:  # if a token don't fall
                return False
        return True

    def update_win(self):
        """
        Draw the win line
        :return: None
        """
        if self.game.winner != TokenState.TokenState.Blank and self.all_win_tokens_are_fall():
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

            if self.win_icon_id != -1:
                self.grid_canvas.delete(self.win_icon_id)

            if self.win_icon_background_id != -1:
                self.grid_canvas.delete(self.win_icon_background_id)

            self.win_icon_background_id = self.grid_canvas.create_image(
                self.grid_canvas.winfo_width() / 2,
                self.grid_canvas.winfo_height() / 2 - self.token_square_size / 2 - 25,
                image=self.ui.image_getter.win_token_background
            )

            self.win_icon_id = self.grid_canvas.create_image(
                self.grid_canvas.winfo_width() / 2,
                self.grid_canvas.winfo_height() / 2 - self.token_square_size / 2 - 25,
                image=self.ui.image_getter.save_token_photos[self.game.winner][self.players[self.game.winner].token]
            )

            self.grid_canvas.disable = True
            self.win_text_frame.place(relx=0.5, y=self.grid_canvas.winfo_height() / 2 + 20,
                                      anchor=tkinter.tix.CENTER)
            self.win_text_label.configure(
                text=self.ui.translation.get_translation("game_panel_win_format").format(
                    self.players[self.game.winner].name),
                fg="green", font=("Arial Bold", 20)
            )
            self.update_idletasks()
            self.grid_canvas.disable = False

        elif self.game.is_win() and self.all_tokens_are_fall():

            if self.win_icon_id != -1:
                self.grid_canvas.delete(self.win_icon_id[0])
                self.grid_canvas.delete(self.win_icon_id[1])

            if self.win_icon_background_id != -1:
                self.grid_canvas.delete(self.win_icon_background_id[0])
                self.grid_canvas.delete(self.win_icon_background_id[1])

            self.win_icon_background_id = (
                self.grid_canvas.create_image(
                    self.grid_canvas.winfo_width() / 2 - self.token_square_size / 2 - 20,
                    self.grid_canvas.winfo_height() / 2 - self.token_square_size / 2 - 30,
                    image=self.ui.image_getter.win_token_background
                ),
                self.grid_canvas.create_image(
                    self.grid_canvas.winfo_width() / 2 + self.token_square_size / 2 + 20,
                    self.grid_canvas.winfo_height() / 2 - self.token_square_size / 2 - 30,
                    image=self.ui.image_getter.win_token_background
                )
            )

            self.win_icon_id = (
                self.grid_canvas.create_image(
                    self.grid_canvas.winfo_width() / 2 - self.token_square_size / 2 - 20,
                    self.grid_canvas.winfo_height() / 2 - self.token_square_size / 2 - 30,
                    image=self.ui.image_getter.save_token_photos[TokenState.TokenState.Player_1]
                    [self.players[TokenState.TokenState.Player_1].token]
                ),
                self.grid_canvas.create_image(
                    self.grid_canvas.winfo_width() / 2 + self.token_square_size / 2 + 20,
                    self.grid_canvas.winfo_height() / 2 - self.token_square_size / 2 - 30,
                    image=self.ui.image_getter.save_token_photos[TokenState.TokenState.Player_2]
                    [self.players[TokenState.TokenState.Player_2].token]
                )
            )

            self.grid_canvas.disable = True
            self.win_text_frame.place(relx=0.5, y=self.grid_canvas.winfo_height() / 2 + 30,
                                      anchor=tkinter.tix.CENTER)
            self.win_text_label.configure(text=self.ui.translation.get_translation("draw"),
                                          fg="green", font=("Arial Bold", 30))
            self.update_idletasks()
            self.grid_canvas.disable = False

    def tick_update(self):
        """
        See panel class
        :return: See panel class
        """

        i = 0
        while i < len(self.token_animation_list):
            try:
                self.token_animation_list[i].tick_update()
            except tkinter.tix.TclError:
                pass

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

    def remove_all_token_animation(self):
        """
        Remove all tokens animations
        :return: None
        """
        while len(self.token_animation_list):
            self.remove_token_animation(self.token_animation_list[0])

    def run_ai_turn(self):
        """
        Run the ai turn
        :return: None
        """
        if isinstance(self.players[self.game.current_turn], AIPlayer.AIPlayer) \
                and not self.players[self.game.current_turn].get_thinking() \
                and not self.game.is_win():
            try:
                self.config(cursor="watch")
                start_time = time.time()
                self.add_token_column(self.players[self.game.current_turn].run_turn())
                print("AI turn run in: {:.2f} second(s)".format(time.time() - start_time))
                self.config(cursor="")
            except tkinter.tix.TclError:
                pass

    def button_main_menu_command(self):
        """
        The command of the button main menu
        :return: None
        """
        from UI.MainMenuPanel import MainMenuPanel
        self.ui.change_panel(MainMenuPanel)

    def button_restart_command(self):
        """
        The command of the button restart
        :return: None
        """
        self.game.reset()
        self.ui.change_panel(GamePanel,
                             player_1=self.players[TokenState.TokenState.Player_1],
                             player_2=self.players[TokenState.TokenState.Player_2],
                             game=self.game,
                             delay=self.delay * 1000)

    def button_back_command(self):
        """
        The command of the button back
        :return: None
        """
        from UI.ConfigureGamePanel import ConfigureGamePanel
        self.ui.change_panel(ConfigureGamePanel)

    def on_end_animation(self, player):
        """
        When a token finish his animation
        :param player: the owner of the token of the animation
        :return: None
        """
        if isinstance(self.players[self.game.current_turn], AIPlayer.AIPlayer) and \
                player == TokenState.TokenState.get_opponent(self.game.current_turn):
            thread = threading.Thread(target=self.run_ai_turn)
            thread.start()

        if self.game.is_win():
            self.update_win()

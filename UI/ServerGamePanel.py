import tkinter.messagebox
import tkinter.tix

from UI import GamePanel, TokenStyle
from main import Player, TokenState
from main.Server import Server, PARAMETER_SEPARATOR

MESSAGE_SET_TURN = "set-turn"
MESSAGE_NEW_TOKEN = "new-token"
MESSAGE_BACK_MENU = "back-to-main-menu"
MESSAGE_RESTART_GAME = "restart"
MESSAGE_SYN = "syn"
SYN_GRID = "G"
SYN_WIN = "W"

SUB_SEPARATOR = '\x02'


class ServerGamePanel(GamePanel.GamePanel):
    """
    The game panel but when you have a server
    """

    def __init__(self, master, ui, is_server=False,
                 player_1=Player.Player(TokenState.TokenState.Player_1, TokenStyle.TokenStyle.Blue),
                 player_2=Player.Player(TokenState.TokenState.Player_2, TokenStyle.TokenStyle.Green),
                 game=None):
        """
        Constructor
        """
        super().__init__(master, ui, player_1, player_2, game, disable_end_button=not is_server)

        self.is_server = is_server

        self.button_syn = tkinter.tix.Button(
            self, image=self.ui.image_getter.syn_icon, command=self.button_syn_command)
        self.button_syn.place(relx=1., rely=0., x=0, y=0, anchor=tkinter.N + tkinter.E)
        self.button_syn_lock = False

        if self.is_server:
            self.after(100, lambda: self.ui.server.send_message_to_all(Server.encode_message(
                PARAMETER_SEPARATOR.join((MESSAGE_SET_TURN, str(self.game.current_turn.value))))))
            self.button_main_menu.configure(
                text=self.ui.translation.get_translation("quit"), command=self.button_back_dialog_command
            )

            # Set server functions
            self.ui.server.on_message_function = self.server_on_message
            self.ui.server.on_client_connect_function = self.server_on_client_connect_function
            self.ui.server.on_client_disconnect_function = self.server_on_client_disconnect_function

        else:
            tkinter.tix.Label(
                self.win_text_frame,
                text=self.ui.translation.get_translation("server_game_wait_host")
            ).grid(row=1, column=0)

            # Set client functions
            self.ui.client.on_message_function = self.client_on_message
            self.ui.client.on_connection_function = self.client_on_connection_function
            self.ui.client.on_disconnection_function = self.client_on_disconnection_function

    def grid_canvas_on_click(self, event):
        """
        When the canvas is click
        :param event: the event
        :return: None
        """
        if event.num == 1:
            column = (event.x - self.width_center) / self.token_square_size
            if 0 <= column <= self.game.grid_width:
                if (self.game.current_turn == TokenState.TokenState.Player_1) == self.is_server:
                    self.add_token_column(int(column))

    def add_token_column(self, column):
        """
        Add a token in the column
        :param column: the column
        :return: if is do
        """
        current_player = self.game.current_turn
        result = super().add_token_column(column)

        if result[0] and (current_player == TokenState.TokenState.Player_1) == self.is_server:
            self.send_add_token(result[1][0], result[1][1])

    def send_add_token(self, x, y):
        """
        Send add token to the player
        :param x: The x coord of the new token
        :param y: The y coord of the new token
        :return: None
        """
        if self.is_server:
            self.ui.server.send_message_to_all(
                Server.encode_message(PARAMETER_SEPARATOR.join((MESSAGE_NEW_TOKEN, str(x), str(y))))
            )
        else:
            self.ui.client.send_message(Server.encode_message(
                PARAMETER_SEPARATOR.join((MESSAGE_NEW_TOKEN, str(x), str(y))))
            )

    def syn_client(self):
        """
        Synchronise the client
        :return: None
        """
        Server.log("Synchronise client", "GamePanel")
        if self.is_server:
            grid_state = ''
            for line in self.game.grid:
                for e in line:
                    grid_state += str(e.value)
                grid_state += SUB_SEPARATOR
            self.ui.server.send_message_to_all(Server.encode_message(PARAMETER_SEPARATOR.join((
                MESSAGE_SYN, SYN_GRID, str(self.game.current_turn.value), grid_state))))

            if self.game.is_win():
                self.ui.server.send_message_to_all(Server.encode_message(PARAMETER_SEPARATOR.join((
                    MESSAGE_SYN,
                    SYN_WIN, str(self.game.winner.value),
                    SUB_SEPARATOR.join(
                        (str(self.game.score[0]), str(self.game.score[1]))),
                    SUB_SEPARATOR.join((
                        ''.join(str(self.game.win_tokens_coord[0])),
                        ''.join(str(self.game.win_tokens_coord[1]))
                    ))
                    ))))
        else:
            self.ui.client.send_message(Server.encode_message(MESSAGE_SYN))

    def destroy(self):
        if self.is_server:
            self.ui.server.on_message_function = lambda message: None
            self.ui.server.on_client_connect_function = lambda client: None
            self.ui.server.on_client_disconnect_function = lambda client: None
        else:
            self.ui.client.on_message_function = lambda message: None
            self.ui.client.on_connection_function = lambda: None
            self.ui.client.on_disconnection_function = lambda: None

        super().destroy()

    def server_on_message(self, message):
        """
        When the server receive a message
        :param message: The message receive
        :return: None
        """
        message = message.split(PARAMETER_SEPARATOR)

        if message[0] == MESSAGE_NEW_TOKEN and len(message) == 3:
            if self.game.current_turn == TokenState.TokenState.Player_1:
                self.syn_client()

            try:
                x = int(message[1])
                y = int(message[2])

                if 0 <= x < self.game.grid_width and \
                        0 <= y < self.game.grid_height:

                    if not self.add_token_with_coord(x, y)[0]:
                        Server.warn("Can't place a token at this coord", "GamePanel")
                        self.syn_client()
                else:
                    Server.warn("X or y is not valid", "GamePanel")
                    self.syn_client()
            except ValueError:
                Server.warn("X or y coord NaN", "GamePanel")
                self.syn_client()

        elif message[0] == MESSAGE_SYN:
            self.syn_client()

    def button_main_menu_command(self):
        """
        When the button main menu is press
        :return: None
        """
        if tkinter.messagebox.askquestion(
                self.ui.translation.get_translation("server_dialog_quit_title"),
                self.ui.translation.get_translation("server_dialog_quit_message")
        ) == tkinter.messagebox.YES:
            if self.is_server:
                self.ui.server.stop_server()
            else:
                self.ui.client.close_connection()

            from UI.ServerListPanel import ServerListPanel
            self.ui.change_panel(ServerListPanel)

    def button_restart_command(self):
        """
        The command of the button restart
        :return: None
        """
        if self.is_server:
            self.ui.server.send_message_to_all(Server.encode_message(MESSAGE_RESTART_GAME))
        self.game.reset()
        self.ui.change_panel(ServerGamePanel,
                             player_1=self.players[TokenState.TokenState.Player_1],
                             player_2=self.players[TokenState.TokenState.Player_2],
                             game=self.game, is_server=self.is_server)

    def button_back_command(self):
        """
        The command of the button back
        :return: None
        """
        if self.is_server:
            from UI.ServerGameConfigurationPanel import ServerGameConfigurationPanel
            self.ui.change_panel(ServerGameConfigurationPanel, is_server=self.is_server)
            self.ui.server.send_message_to_all(Server.encode_message(MESSAGE_BACK_MENU))
        else:
            if tkinter.messagebox.askquestion(
                    self.ui.translation.get_translation("server_dialog_quit_title"),
                    self.ui.translation.get_translation("server_dialog_quit_message")
            ) == tkinter.messagebox.YES:
                from UI.ServerListPanel import ServerListPanel
                self.ui.client.close_connection()
                self.ui.change_panel(ServerListPanel)

    def button_back_dialog_command(self):
        """
        The command of the button main menu (top left corner)
        :return: None
        """
        if self.is_server and tkinter.messagebox.askquestion(
                self.ui.translation.get_translation("server_dialog_back_title"),
                self.ui.translation.get_translation("server_dialog_back_message")
        ) == tkinter.messagebox.YES:
            self.button_back_command()

    def button_syn_command(self):
        """
        Synchronise the client button
        :return: None
        """
        if not self.button_syn_lock:
            self.button_syn_lock = True
            self.syn_client()
            self.after(1000, self.button_syn_unlock)

    def button_syn_unlock(self):
        """
        Unlock lock
        :return: None
        """
        self.button_syn_lock = False

    def server_on_client_connect_function(self, client):
        """
        When the server detect a connection
        :param client: The socket of the client
        :return: None
        """

    # noinspection PyUnusedLocal
    def server_on_client_disconnect_function(self, client):
        """
        When the server detect a disconnection
        :param client: The socket of the client
        :return: None
        """
        from UI.ServerGameConfigurationPanel import ServerGameConfigurationPanel
        self.ui.change_panel(ServerGameConfigurationPanel, is_server=True)

    def client_on_message(self, message):
        """
        When the client receive a message
        :param message: The message receive
        :return: None
        """
        message = message.split(PARAMETER_SEPARATOR)

        if message[0] == MESSAGE_SET_TURN and len(message) == 2:
            self.game.current_turn = TokenState.TokenState(int(message[1]))
            self.update_turn_label()

        elif message[0] == MESSAGE_NEW_TOKEN and len(message) == 3:
            if self.game.current_turn == TokenState.TokenState.Player_2:
                self.syn_client()
                return

            try:
                x = int(message[1])
                y = int(message[2])

                if 0 <= x < self.game.grid_width and \
                        0 <= y < self.game.grid_height:

                    if not self.add_token_with_coord(x, y)[0]:
                        Server.warn("Can't place a token at this coord", "GamePanel")
                        self.syn_client()
                else:
                    Server.warn("X or y is not valid", "GamePanel")
                    self.syn_client()
            except ValueError:
                Server.warn("X or y coord NaN", "GamePanel")
                self.syn_client()

        elif message[0] == MESSAGE_BACK_MENU:
            from UI.ServerGameConfigurationPanel import ServerGameConfigurationPanel
            self.ui.change_panel(ServerGameConfigurationPanel, is_server=False)

        elif message[0] == MESSAGE_RESTART_GAME:
            self.button_restart_command()

        elif message[0] == MESSAGE_SYN and 3 < len(message) < 6:
            if message[1] == SYN_GRID:
                try:
                    current_token = TokenState.TokenState(int(message[2]))
                    if self.game.current_turn != current_token:
                        self.game.current_turn = current_token
                        self.update_turn_label()
                except ValueError:
                    pass

                split = message[3].split(SUB_SEPARATOR)
                if len(split) == self.game.grid_width and len(split[0]) == self.game.grid_height:
                    for x, line in enumerate(split):
                        for y, e in enumerate(line):
                            token = TokenState.TokenState(int(e))
                            if self.game.grid[x][y] != token:
                                self.game.grid[x][y] = token
                                self.update_image(x, y)
            else:
                try:
                    self.game.winner = TokenState.TokenState(int(message[2]))
                except ValueError:
                    pass

                scores = message[3].split(SUB_SEPARATOR)
                if len(scores) == 2:
                    scores[0], scores[1] = int(scores[0]), int(scores[1])
                    self.game.score = scores

                token_coord = message[4].split(SUB_SEPARATOR)  # xy|xy
                if len(token_coord) == 2 and len(token_coord[0]) == 2:
                    for i, c in enumerate(token_coord):
                        for j, xy in enumerate(c):
                            self.game.win_tokens_coord[i][j] = xy

                    self.game.win_tokens_coord = token_coord

                self.update_win()

    def client_on_connection_function(self):
        """
        When the client is connect
        :return: None
        """

    def client_on_disconnection_function(self):
        """
        When the client is disconnect
        :return: None
        """
        from UI.ServerListPanel import ServerListPanel
        self.ui.change_panel(ServerListPanel)

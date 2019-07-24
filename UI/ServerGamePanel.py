from UI import GamePanel, TokenStyle
from main import Player, TokenState, Game, Server

MESSAGE_NEW_TOKEN = "new-token"
MESSAGE_BACK_MENU = "back-to-main-menu"


class ServerGamePanel(GamePanel.GamePanel):
    """
    The game panel but when you have a server
    """

    def __init__(self, master, ui, is_server=False,
                 player_1=Player.Player(TokenState.TokenState.Player_1, TokenStyle.TokenStyle.Blue),
                 player_2=Player.Player(TokenState.TokenState.Player_2, TokenStyle.TokenStyle.Green),
                 game=Game.Game()):
        """
        Constructor
        """
        super().__init__(master, ui, player_1, player_2, game)

        self.button_main_menu.configure(
            text=self.ui.translation.get_translation("back")
        )

        self.is_server = is_server

        if self.is_server:
            # Set server functions
            self.ui.server.on_message_function = self.server_on_message
            self.ui.server.on_client_connect_function = self.server_on_client_connect_function
            self.ui.server.on_client_disconnect_function = self.server_on_client_disconnect_function

        else:
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
                Server.Server.encode_message('_'.join((MESSAGE_NEW_TOKEN, str(x), str(y))))
            )
        else:
            self.ui.client.send_message(Server.Server.encode_message(
                '_'.join((MESSAGE_NEW_TOKEN, str(x), str(y))))
            )

    def destroy(self):
        if self.is_server:
            self.ui.server.on_message_function = lambda message: None
            self.ui.server.on_client_connect_function = lambda client: None
            self.ui.server.on_client_disconnect_function = lambda client: None
        else:
            self.ui.client.on_message_function = lambda message: None
            self.ui.client.on_connection_function = lambda: None
            self.ui.client.on_disconnection_function = lambda: None

        self.remove_all_token_animation()
        self.grid_canvas.remove_resizing()

        super().destroy()

    def server_on_message(self, message):
        """
        When the server receive a message
        :param message: The message receive
        :return: None
        """
        messages = Server.Server.decode_message(message)

        for message in messages:
            message = message.split('_')

            if message[0] == MESSAGE_NEW_TOKEN and \
                    not ((self.game.current_turn == TokenState.TokenState.Player_1) == self.is_server):

                try:
                    x = int(message[1])
                    y = int(message[2])

                    if 0 <= x < self.game.grid_width and \
                            0 <= y < self.game.grid_height:

                        if not self.add_token_with_coord(x, y)[0]:
                            Server.Server.warn("Can't place a token at this coord", "GamePanel")
                    else:
                        Server.Server.warn("X or y is not valid", "GamePanel")
                except ValueError:
                    Server.Server.warn("X or y coord NaN", "GamePanel")

    def button_main_menu_command(self):
        """
        When the button main menu is press
        :return: None
        """
        if self.is_server:
            from UI.ServerGameConfigurationPanel import ServerGameConfigurationPanel
            self.ui.change_panel(ServerGameConfigurationPanel, create_game=self.is_server)  # TODO sync server on
            self.ui.server.send_message_to_all(Server.Server.encode_message(MESSAGE_BACK_MENU))
        else:
            from UI.ServerListPanel import ServerListPanel
            self.ui.client.close_connection()
            self.ui.change_panel(ServerListPanel)

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
        self.ui.change_panel(ServerGameConfigurationPanel, create_game=self.is_server)  # TODO sync server on

    def client_on_message(self, message):
        """
        When the client receive a message
        :param message: The message receive
        :return: None
        """
        messages = Server.Server.decode_message(message)

        for message in messages:
            message = message.split('_')

            if message[0] == MESSAGE_NEW_TOKEN and \
                    not ((self.game.current_turn == TokenState.TokenState.Player_1) == self.is_server):

                try:
                    x = int(message[1])
                    y = int(message[2])

                    if 0 <= x < self.game.grid_width and \
                            0 <= y < self.game.grid_height:

                        if not self.add_token_with_coord(x, y)[0]:
                            Server.Server.warn("Can't place a token at this coord", "GamePanel")
                    else:
                        Server.Server.warn("X or y is not valid", "GamePanel")
                except ValueError:
                    Server.Server.warn("X or y coord NaN", "GamePanel")

            elif message[0] == MESSAGE_BACK_MENU:
                from UI.ServerGameConfigurationPanel import ServerGameConfigurationPanel
                self.ui.change_panel(ServerGameConfigurationPanel, create_game=self.is_server)  # TODO sync server on

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

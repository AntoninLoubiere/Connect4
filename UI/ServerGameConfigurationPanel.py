import errno
import random
import tkinter.messagebox
import tkinter.tix

import main.Preferences
from UI import Panel, TokenStyle, ServerGamePanel, ImageGetter, ConfigureGamePanel
from UI.ConfigureGamePanel import TOKEN_MARGIN
from main import Server, Player, Game
from main.TokenState import TokenState

MESSAGE_NEED_STATE = "need-state"
MESSAGE_SEND_TOKEN_SELECTED = "token-selected"
MESSAGE_SEND_NAME_SELECTED = "player-name"
MESSAGE_SEND_READY = "player-2-is-ready"
MESSAGE_PLAYER_1_WANT_START = "player-1-want-start"
MESSAGE_PLAY = "play"

SERVER_ERROR_DIALOG_KEY_FORMAT = "server_start_error_{}_dialog_message"  # {} is error name


class ServerGameConfigurationPanel(Panel.Panel):
    """
    The configuration panel of the server and the game
    """

    def __init__(self, master, ui, create_game=False):
        """
        Constructor
        """
        super().__init__(master, ui)
        self.create_game = create_game

        self.player_2_is_ready = False
        self.player_2_is_connected = False

        for r in range(2, 3):
            self.rowconfigure(r, weight=1)

        for c in range(0, 2):
            self.columnconfigure(c, weight=1)

        self.player = (TokenState.Player_2, TokenState.Player_1)[create_game]
        self.player_id = (1, 0)[create_game]
        self.opponent = (TokenState.Player_1, TokenState.Player_2)[create_game]
        self.opponent_id = (0, 1)[create_game]

        self.ui.image_getter.resize_tokens_images(100)

        # Configure server

        if create_game:

            self.server_configure_frame = tkinter.tix.Frame(
                self, relief=tkinter.tix.SUNKEN, borderwidth=2,
                padx=10, pady=10
            )
            self.server_configure_frame.grid(row=0, column=0, columnspan=2, sticky=tkinter.tix.NSEW, padx=10, pady=10)

            for c in range(0, 2):
                self.server_configure_frame.columnconfigure(c, weight=1)

            self.server_state_label = tkinter.tix.Label(
                self.server_configure_frame, text=self.ui.translation.get_translation("server_state_stopped"),
                fg="#ee2e31"
            )
            self.server_state_label.grid(row=0, column=0, columnspan=2, sticky=tkinter.tix.NSEW)

            self.server_host = tkinter.tix.Label(
                self.server_configure_frame,
                text=self.ui.translation.get_translation("server_configuration_host_label").format(
                    Server.Server.get_ip())
            )

            self.server_host.grid(row=1, column=0, sticky=tkinter.tix.NSEW)

            self.server_port_frame = tkinter.tix.Frame(self.server_configure_frame)
            self.server_port_frame.grid(row=1, column=1, sticky=tkinter.tix.NSEW)

            for c in range(0, 2):
                self.server_port_frame.columnconfigure(c, weight=1)

            self.server_port_label = tkinter.tix.Label(
                self.server_port_frame,
                text=self.ui.translation.get_translation("server_configuration_port_entry_title")
            )
            self.server_port_label.grid(row=0, column=0, sticky=tkinter.tix.E)

            self.server_port_spin_box = tkinter.tix.Spinbox(self.server_port_frame, from_=3000, to=3020, wrap=True)
            self.server_port_spin_box.grid(row=0, column=1, sticky=tkinter.tix.W)

            self.server_action_frame = tkinter.tix.Frame(self.server_configure_frame)
            self.server_action_frame.grid(row=2, column=0, columnspan=2, sticky=tkinter.tix.NSEW)

            for c in range(0, 3):
                self.server_action_frame.columnconfigure(c, weight=1)

            self.server_start_stop = tkinter.tix.Button(
                self.server_action_frame, text=self.ui.translation.get_translation("server_configuration_start"),
                command=self.server_start_stop_command
            )
            self.server_start_stop.grid(row=0, column=0, sticky=tkinter.tix.NSEW)

            if self.ui.server.server_is_on:
                self.server_port_spin_box.configure(state="readonly", increment=0)
                self.server_start_stop.configure(
                    text=self.ui.translation.get_translation("server_configuration_stop")
                )

                self.server_state_label.configure(
                    text=self.ui.translation.get_translation("server_state_started"), fg="#78bc61"
                )

        # Configure game

        self.players_name_frame = [tkinter.tix.Frame(self),
                                   tkinter.tix.Frame(self)]
        self.players_name_frame[0].grid(row=1, column=0)
        self.players_name_frame[1].grid(row=1, column=1)

        tkinter.tix.Label(self.players_name_frame[0], text=self.ui.translation.get_translation(
            "configure_game_panel_name")).grid(row=0, column=0)
        tkinter.tix.Label(self.players_name_frame[1], text=self.ui.translation.get_translation(
            "configure_game_panel_name")).grid(row=0, column=0)

        self.players_entry_string_variable = [
            tkinter.tix.StringVar(),
            tkinter.tix.StringVar()
        ]

        for i in range(0, 2):
            if i == self.opponent_id:
                self.players_entry_string_variable[i].set(
                    self.ui.translation.get_translation("server_configuration_waiting"))
            else:
                self.players_entry_string_variable[i].set(
                    self.ui.translation.get_translation("default_player_name").format(str(i + 1))
                )

        self.players_entry = [tkinter.tix.Entry(self.players_name_frame[0],
                                                textvariable=self.players_entry_string_variable[0],
                                                state=("readonly", "normal")[create_game]),
                              tkinter.tix.Entry(self.players_name_frame[1],
                                                textvariable=self.players_entry_string_variable[1],
                                                state=("normal", "readonly")[create_game])]

        if create_game:
            self.players_entry_string_variable[0].trace_add("write", lambda x, y, z: self.name_string_var_trace_write())
        else:
            self.players_entry_string_variable[1].trace_add("write", lambda x, y, z: self.name_string_var_trace_write())

        self.players_entry[0].grid(row=0, column=1)
        self.players_entry[1].grid(row=0, column=1)

        self.players_settings_scrolled_window = [tkinter.tix.ScrolledWindow(self, relief=tkinter.tix.SUNKEN,
                                                                            borderwidth=3),
                                                 tkinter.tix.ScrolledWindow(self, relief=tkinter.tix.SUNKEN,
                                                                            borderwidth=3)]
        self.players_settings_scrolled_window[0].grid(row=2, column=0, sticky=tkinter.tix.NSEW, pady=10, padx=5)
        self.players_settings_scrolled_window[1].grid(row=2, column=1, sticky=tkinter.tix.NSEW, pady=10, padx=5)

        self.players_settings_window = [self.players_settings_scrolled_window[0].window,
                                        self.players_settings_scrolled_window[1].window]

        for i in range(0, 2):
            self.players_settings_window[i].grid_columnconfigure(0, weight=1)

        self.players_tokens = [
            TokenStyle.TokenStyle(random.randint(0, TokenStyle.NUMBER_STYLE - 1)),
            TokenStyle.TokenStyle(random.randint(0, TokenStyle.NUMBER_STYLE - 1))
        ]
        self.players_tokens[self.opponent_id] = TokenStyle.TokenStyle.Not_Connected

        self.players_tokens_images = [
            self.ui.image_getter.save_token_photos[TokenState.Player_1][self.players_tokens[0]],
            self.ui.image_getter.save_token_photos[TokenState.Player_2][self.players_tokens[1]]
        ]

        self.players_tokens_labels = [
            tkinter.tix.Label(self.players_settings_window[0], image=self.players_tokens_images[0]),
            tkinter.tix.Label(self.players_settings_window[1], image=self.players_tokens_images[1])
        ]

        self.players_tokens_labels[0].grid(row=1, column=0, sticky=tkinter.tix.NSEW)
        self.players_tokens_labels[1].grid(row=1, column=0, sticky=tkinter.tix.NSEW)

        self.player_1_label = tkinter.tix.Label(
            self.players_settings_window[0], fg="white", text="", wraplength=250
        )
        self.player_1_label.grid(row=2, column=0)

        self.player_2_ready_label = tkinter.tix.Label(
            self.players_settings_window[1], fg="#ee2e31",
            text=self.ui.translation.get_translation(
                ("server_configuration_player_2_not_ready",
                 "server_configuration_player_2_not_connected")
                [self.create_game])
        )
        self.player_2_ready_label.grid(row=2, column=0)

        self.button_token_choose_per_line_last = 0
        self.button_token_choose_per_line = 0

        self.token_choose_frame = tkinter.tix.Frame(self.players_settings_window[self.player_id])

        self.token_choose_frame.grid(row=3, column=0, sticky=tkinter.tix.NSEW)

        self.token_choose_buttons = []

        for index in range(0, TokenStyle.NUMBER_STYLE):
            self.token_choose_buttons.append(tkinter.tix.Button(self.token_choose_frame,
                                                                image=self.ui.image_getter.save_token_icons[self.player]
                                                                [TokenStyle.TokenStyle(index)],
                                                                command=lambda _index=index:
                                                                self.button_change_token_command(
                                                                    _index)))

        self.button_main_menu = tkinter.tix.Button(
            self,
            text=self.ui.translation.get_translation("back"),
            command=self.button_main_menu_command)
        self.button_main_menu.grid(row=3, column=0, sticky=tkinter.tix.NSEW)

        self.button_play = tkinter.tix.Button(
            self,
            text=self.ui.translation.get_translation(("ready", "play")[create_game]),
            command=self.button_play_command)
        if not self.create_game:
            self.button_play.configure(fg="#ee2e31", activeforeground="#ee2e31")
        self.button_play.grid(row=3, column=1, sticky=tkinter.tix.NSEW)

        self.import_last_game_setting()

        if create_game:
            # Set server functions
            self.ui.server.on_message_function = self.server_on_message
            self.ui.server.on_client_connect_function = self.server_on_client_connect_function
            self.ui.server.on_client_disconnect_function = self.server_on_client_disconnect_function

        else:
            # Set client functions
            self.ui.client.on_message_function = self.client_on_message
            self.ui.client.on_connection_function = self.client_on_connection_function
            self.ui.client.on_disconnection_function = self.client_on_disconnection_function

            self.client_on_connection_function()  # because it is already connected

    def on_create_finish(self):
        """
        When the panel is pack (See panel class)
        :return: None
        """
        self.on_resize(None)

    def on_resize(self, event):
        """
        When the panel is resize (see in panel class)
        :param event: the tkinter event
        :return: None
        """
        self.recreate_tokens_buttons()
        self.columnconfigure(0, minsize=self.winfo_width() / 2)
        self.columnconfigure(1, minsize=self.winfo_width() / 2)
        self.player_1_label.configure(wraplength=self.players_settings_window[0].winfo_width() - 10)
        super().on_resize(event)

    def recreate_tokens_buttons(self):
        """
        Recreate tokens buttons
        :return: None
        """
        self.button_token_choose_per_line_last = self.button_token_choose_per_line
        self.button_token_choose_per_line = max(
            min(
                int(self.players_settings_window[self.player_id].winfo_width()
                    / (ImageGetter.TOKEN_ICON_SIZE + TOKEN_MARGIN)),
                TokenStyle.NUMBER_STYLE,
            ),
            1
        )

        for i in range(0, max(self.button_token_choose_per_line, self.button_token_choose_per_line_last)):
            if i < self.button_token_choose_per_line:
                self.token_choose_frame.columnconfigure(i, weight=1)
            else:
                self.token_choose_frame.columnconfigure(i, weight=0)

        for index in range(0, TokenStyle.NUMBER_STYLE):
            if index % self.button_token_choose_per_line == 0:
                self.token_choose_frame.rowconfigure(int(index / self.button_token_choose_per_line), pad=3)

            self.token_choose_buttons[index].grid(row=int(index / self.button_token_choose_per_line),
                                                  column=index % self.button_token_choose_per_line)

    def import_last_game_setting(self):
        """
        Import the preferences set in the last game
        :return: None
        """
        if self.ui.preference.temporary_preference_exist(main.Preferences.TEMPORARY_PREFERENCES_PLAYERS_NAMES):
            self.players_entry_string_variable[self.player_id].set(
                self.ui.preference.get_temporary_preference(main.Preferences.TEMPORARY_PREFERENCES_PLAYERS_NAMES)
                [0])

        if self.ui.preference.temporary_preference_exist(main.Preferences.TEMPORARY_PREFERENCES_PLAYERS_TOKENS):
            tokens = self.ui.preference.get_temporary_preference(main.Preferences.TEMPORARY_PREFERENCES_PLAYERS_TOKENS)

            self.players_tokens[self.player_id] = tokens[0]

            self.players_tokens_images[self.player_id] = \
                self.ui.image_getter.save_token_photos[self.player][self.players_tokens[self.player_id]]

            self.players_tokens_labels[self.player_id].config(image=self.players_tokens_images[self.player_id])

    def export_last_game_settings(self):
        """
        Export setting to save the preference of the last game
        :return: None
        """

        players_names = [
            self.players_entry_string_variable[self.player_id].get(),
            self.ui.translation.get_translation("default_player_name").format("2")
        ]

        self.ui.preference.set_temporary_preference(main.Preferences.TEMPORARY_PREFERENCES_PLAYERS_NAMES, players_names)

        tokens_player = [
            self.players_tokens[self.player_id],
            TokenStyle.TokenStyle(random.randint(0, TokenStyle.NUMBER_STYLE - 1))
        ]

        self.ui.preference.set_temporary_preference(main.Preferences.TEMPORARY_PREFERENCES_PLAYERS_TOKENS,
                                                    tokens_player)

    def server_start_stop_command(self):
        """
        Start the server
        :return: None
        """
        if self.ui.server.server_is_on:
            if not self.player_2_is_connected or tkinter.messagebox.askquestion(
                    self.ui.translation.get_translation("server_dialog_server_stop_title"),
                    self.ui.translation.get_translation("server_dialog_server_stop_message")
            ) == tkinter.messagebox.YES:
                if self.ui.server.stop_server():
                    self.server_port_spin_box.configure(state=tkinter.tix.NORMAL, increment=1)
                    self.server_start_stop.configure(
                        text=self.ui.translation.get_translation("server_configuration_start")
                    )

                    self.server_state_label.configure(
                        text=self.ui.translation.get_translation("server_state_stopped"),
                        fg="#ee2e31"
                    )
        else:
            try:
                port = int(self.server_port_spin_box.get())
            except ValueError:
                tkinter.messagebox.showerror(
                    self.ui.translation.get_translation("server_configuration_dialog_port_error_title"),
                    self.ui.translation.get_translation("server_configuration_dialog_port_error_message")
                )

            else:
                if 3000 <= port <= 3020:
                    self.ui.server = Server.Server(
                        port=port, max_clients_connected=1,
                        on_message_function=self.server_on_message,
                        on_client_connect_function=self.server_on_client_connect_function,
                        on_client_disconnect_function=self.server_on_client_disconnect_function
                    )
                    result = self.ui.server.start_server()
                    if result[0]:
                        self.server_port_spin_box.configure(state="readonly", increment=0)
                        self.server_start_stop.configure(
                            text=self.ui.translation.get_translation("server_configuration_stop")
                        )

                        self.server_state_label.configure(
                            text=self.ui.translation.get_translation("server_state_started"), fg="#78bc61"
                        )
                    else:
                        error_name = errno.errorcode[result[1]]
                        if self.ui.translation.translation_exist(SERVER_ERROR_DIALOG_KEY_FORMAT.format(error_name)):
                            tkinter.messagebox.showerror(
                                self.ui.translation.get_translation("server_start_error_dialog_title")
                                    .format(result[1]),
                                self.ui.translation.get_translation(SERVER_ERROR_DIALOG_KEY_FORMAT.format(error_name))
                            )
                        else:
                            tkinter.messagebox.showerror(
                                self.ui.translation.get_translation("server_start_error_dialog_title")
                                    .format(result[1]),
                                self.ui.translation.get_translation("server_start_error_unknown_dialog_message")
                                    .format(result[1], error_name, result[2].strerror)
                            )

                else:
                    tkinter.messagebox.showerror(
                        self.ui.translation.get_translation("server_configuration_dialog_port_error_title"),
                        self.ui.translation.get_translation("server_configuration_dialog_port_error_message")
                    )

    def button_main_menu_command(self):
        """
        When the main menu button is press
        :return: None
        """
        if tkinter.messagebox.askquestion(
                self.ui.translation.get_translation("server_dialog_quit_title"),
                self.ui.translation.get_translation("server_dialog_quit_message")
        ) == tkinter.messagebox.YES:
            self.export_last_game_settings()

            if self.ui.server.server_is_on:
                self.ui.server.stop_server()

            from UI.ServerListPanel import ServerListPanel
            self.ui.change_panel(ServerListPanel)

            if self.ui.client is not None and self.ui.client.connected:
                self.ui.client.close_connection()

    def button_change_token_command(self, index):
        """
        When a button to change token is clicked
        :param index: the index of the button
        :return: None
        """
        self.players_tokens[self.player_id] = TokenStyle.TokenStyle(index)

        self.players_tokens_images[self.player_id] = \
            self.ui.image_getter.save_token_photos[self.player][self.players_tokens[self.player_id]]

        self.players_tokens_labels[self.player_id].config(image=self.players_tokens_images[self.player_id])

        if self.create_game:
            self.server_send_token()
        else:
            self.client_send_token()

    def button_play_command(self):
        """
        When the button play (or ready is press)
        :return: None
        """

        if self.create_game:
            if self.player_2_is_connected:
                if self.player_2_is_ready:
                    self.export_last_game_settings()

                    self.ui.change_panel(
                        ServerGamePanel.ServerGamePanel,
                        player_1=Player.Player(TokenState.Player_1, self.players_tokens[0],
                                               self.players_entry_string_variable[0].get()),
                        player_2=Player.Player(TokenState.Player_2, self.players_tokens[1],
                                               self.players_entry_string_variable[1].get()),
                        is_server=self.create_game,
                        game=Game.Game(first_player=random.choice((TokenState.Player_1, TokenState.Player_2)))
                    )

                    self.ui.server.send_message_to_all(Server.Server.encode_message(
                        '_'.join((MESSAGE_PLAY, str(self.ui.current_panel.game.current_turn.value))))
                    )
                else:
                    self.player_1_want_to_start()
        else:
            self.set_player_2_ready(not self.player_2_is_ready)
            self.ui.client.send_message(Server.Server.encode_message('_'.join((MESSAGE_SEND_READY,
                                                                               str(self.player_2_is_ready)))))

    def destroy(self):
        if self.create_game:
            self.ui.server.on_message_function = lambda message: None
            self.ui.server.on_client_connect_function = lambda client: None
            self.ui.server.on_client_disconnect_function = lambda client: None
        else:
            self.ui.client.on_message_function = lambda message: None
            self.ui.client.on_connection_function = lambda: None
            self.ui.client.on_disconnection_function = lambda: None

        super().destroy()

    def player_1_want_to_start(self):
        """
        When the player click on the button play and the second player isn't ready
        :return: None
        """
        self.player_1_label.configure(
            text=self.ui.translation.get_translation("server_configuration_player_1_want_start"), bg="#ee2e31"
        )
        if self.create_game:
            self.ui.server.send_message_to_all(Server.Server.encode_message(MESSAGE_PLAYER_1_WANT_START))

    def set_player_2_ready(self, value):
        """
        Set if the player 2 is ready
        :param value: If the player 2 is ready
        :return: None
        """
        self.player_2_is_ready = value

        if self.player_2_is_ready:
            self.player_2_ready_label.configure(
                text=self.ui.translation.get_translation("server_configuration_player_2_ready"), fg="#78bc61"
            )
        else:
            if not self.player_2_is_connected and self.create_game:
                self.player_2_ready_label.configure(
                    text=self.ui.translation.get_translation("server_configuration_player_2_not_connected"),
                    fg="#ee2e31"
                )
            else:
                self.player_2_ready_label.configure(
                    text=self.ui.translation.get_translation("server_configuration_player_2_not_ready"), fg="#ee2e31"
                )

        if not self.create_game:
            if self.player_2_is_ready:
                self.button_play.configure(
                    text=self.ui.translation.get_translation("not_ready"), fg="#78bc61", activeforeground="#78bc61"
                )

            else:
                self.button_play.configure(
                    text=self.ui.translation.get_translation("ready"), fg="#ee2e31", activeforeground="#ee2e31"
                )

        self.player_1_label.configure(text="", bg=self.cget("bg"))

    def name_string_var_trace_write(self, send_update=True):
        """
        The trace function of names strings vars
        :return: None
        """
        self.players_entry[0].configure(
            fg=("black", "#ee2e31")[len(self.players_entry_string_variable[0].get().strip()) < 3]
        )
        self.players_entry[1].configure(
            fg=("black", "#ee2e31")[len(self.players_entry_string_variable[1].get().strip()) < 3]
        )
        if self.player_2_is_connected:
            if len(self.players_entry_string_variable[0].get().strip()) >= 3 and \
                    self.players_entry_string_variable[0].get().strip() == \
                    self.players_entry_string_variable[1].get().strip():
                self.players_entry[0].configure(fg="#ee8f2f")
                self.players_entry[1].configure(fg="#ee8f2f")

        if send_update:
            if self.create_game:
                self.server_send_player_name()
            else:
                self.client_send_player_name()

        if len(self.players_entry_string_variable[0].get()) > ConfigureGamePanel.NAME_MAX_VALUE:
            self.players_entry_string_variable[0].set(self.players_entry_string_variable[0].get()
                                                      [:ConfigureGamePanel.NAME_MAX_VALUE])

        if len(self.players_entry_string_variable[1].get()) > ConfigureGamePanel.NAME_MAX_VALUE:
            self.players_entry_string_variable[1].set(self.players_entry_string_variable[1].get()
                                                      [:ConfigureGamePanel.NAME_MAX_VALUE])

    def server_on_message(self, message):
        """
        When the server receive a message
        :param message: The message receive
        :return: None
        """
        messages = Server.Server.decode_message(message)

        for message in messages:
            message = message.split('_')
            if message[0] == MESSAGE_NEED_STATE:
                self.server_send_player_name()
                self.server_send_token()
                self.player_2_ready_label.configure(
                    text=self.ui.translation.get_translation("server_configuration_player_2_not_ready")
                )
                self.player_2_is_connected = True

            elif message[0] == MESSAGE_SEND_NAME_SELECTED:
                self.players_entry_string_variable[1].set(message[1])
                self.name_string_var_trace_write(False)

            elif message[0] == MESSAGE_SEND_TOKEN_SELECTED:
                try:
                    # noinspection PyTypeChecker
                    self.players_tokens[self.opponent_id] = TokenStyle.TokenStyle(int(message[1]))

                    self.players_tokens_images[self.opponent_id] = \
                        self.ui.image_getter.save_token_photos[self.opponent][self.players_tokens[self.opponent_id]]

                    self.players_tokens_labels[self.opponent_id].config(
                        image=self.players_tokens_images[self.opponent_id]
                    )
                except ValueError:
                    pass
            elif message[0] == MESSAGE_SEND_READY:
                self.set_player_2_ready(message[1] == "True")

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
        self.set_player_2_ready(False)
        self.player_2_is_connected = self.ui.server.get_number_client() >= 1
        if not self.player_2_is_connected:
            self.player_1_label.configure(bg=self.cget("bg"), text="")

            self.player_2_ready_label.configure(
                text=self.ui.translation.get_translation("server_configuration_player_2_not_connected"),
                fg="#ee2e31"
            )

            self.players_entry_string_variable[self.opponent_id].set(
                self.ui.translation.get_translation("server_configuration_waiting")
            )

            self.players_tokens[self.opponent_id] = TokenStyle.TokenStyle.Not_Connected

            self.players_tokens_images[self.opponent_id] = \
                self.ui.image_getter.save_token_photos[self.opponent][self.players_tokens[self.opponent_id]]

            self.players_tokens_labels[self.opponent_id].config(image=self.players_tokens_images[self.opponent_id])

    def server_send_player_name(self):
        """
        Send the name of the host player
        :return: None
        """
        self.ui.server.send_message_to_all(Server.Server.encode_message(
            '_'.join((MESSAGE_SEND_NAME_SELECTED, self.players_entry_string_variable[self.player_id].get())))
        )

    def server_send_token(self):
        """
        Send the token of the client
        :return: None
        """
        self.ui.server.send_message_to_all(Server.Server.encode_message(
            '_'.join((MESSAGE_SEND_TOKEN_SELECTED, str(self.players_tokens[self.player_id].value))))
        )

    def client_on_message(self, message):
        """
        When the client receive a message
        :param message: The message receive
        :return: None
        """
        messages = Server.Server.decode_message(message)

        for message in messages:
            message = message.split('_')

            if message[0] == MESSAGE_NEED_STATE:
                self.client_send_player_name()
                self.client_send_token()

            elif message[0] == MESSAGE_SEND_NAME_SELECTED:
                self.players_entry_string_variable[0].set(message[1])
                self.name_string_var_trace_write(False)

            elif message[0] == MESSAGE_SEND_TOKEN_SELECTED:
                try:
                    # noinspection PyTypeChecker
                    self.players_tokens[self.opponent_id] = TokenStyle.TokenStyle(int(message[1]))

                    self.players_tokens_images[self.opponent_id] = \
                        self.ui.image_getter.save_token_photos[self.opponent][self.players_tokens[self.opponent_id]]

                    self.players_tokens_labels[self.opponent_id].config(
                        image=self.players_tokens_images[self.opponent_id]
                    )
                except ValueError:
                    pass

            elif message[0] == MESSAGE_PLAYER_1_WANT_START:
                self.player_1_want_to_start()

            elif message[0] == MESSAGE_PLAY:
                game = Game.Game(first_player=(TokenState.Player_2, TokenState.Player_1)[message[1] == "1"])

                self.export_last_game_settings()

                self.ui.change_panel(
                    ServerGamePanel.ServerGamePanel,
                    player_1=Player.Player(TokenState.Player_1, self.players_tokens[0],
                                           self.players_entry_string_variable[0].get()),
                    player_2=Player.Player(TokenState.Player_2, self.players_tokens[1],
                                           self.players_entry_string_variable[1].get()),
                    is_server=self.create_game,
                    game=game
                )

    def client_on_connection_function(self):
        """
        When the client is connect
        :return: None
        """
        self.ui.client.send_message(Server.Server.encode_message(MESSAGE_NEED_STATE))
        self.client_send_player_name()
        self.client_send_token()

    def client_on_disconnection_function(self):
        """
        When the client is disconnect
        :return: None
        """
        from UI.ServerListPanel import ServerListPanel
        self.ui.change_panel(ServerListPanel)

    def client_send_player_name(self):
        """
        Send the name of the client player
        :return:
        """
        self.ui.client.send_message(Server.Server.encode_message(
            '_'.join((MESSAGE_SEND_NAME_SELECTED, self.players_entry_string_variable[self.player_id].get())))
        )

    def client_send_token(self):
        """
        Send the token of the client
        :return: None
        """
        self.ui.client.send_message(Server.Server.encode_message(
            '_'.join((MESSAGE_SEND_TOKEN_SELECTED, str(self.players_tokens[self.player_id].value))))
        )

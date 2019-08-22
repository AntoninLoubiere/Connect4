import random
import tkinter.messagebox
import tkinter.tix

from UI import Panel, GamePanel, MainMenuPanel, TokenStyle, ImageGetter
from main import Game, AIPlayer, Player
from main.Preferences import TEMPORARY_PREFERENCES_PLAYERS_TOKENS, TEMPORARY_PREFERENCES_PLAYERS_AI, \
    TEMPORARY_PREFERENCES_PLAYERS_NAMES, TEMPORARY_PREFERENCES_DIFFICULTY, \
    PREFERENCE_DELAY, PREFERENCE_DIFFICULTY_LEVEl
from main.TokenState import TokenState

DEFAULT_BUTTON_DIFFICULTY_SELECT = 2

TOKEN_MARGIN = 10


class ConfigureGamePanel(Panel.Panel):
    """
    The panel which configure the game, chose skin...
    """

    def __init__(self, master, ui):
        super().__init__(master, ui)
        self.ui.image_getter.resize_tokens_images(100)

        for i in range(0, 2):
            self.grid_columnconfigure(i, weight=1)

        for i in range(1, 2):
            self.grid_rowconfigure(i, weight=1)

        self.players_name_frame = [tkinter.tix.Frame(self),
                                   tkinter.tix.Frame(self)]
        self.players_name_frame[0].grid(row=0, column=0)
        self.players_name_frame[1].grid(row=0, column=1)

        tkinter.tix.Label(self.players_name_frame[0], text=self.ui.translation.get_translation(
            "configure_game_panel_name")).grid(row=0, column=0)
        tkinter.tix.Label(self.players_name_frame[1], text=self.ui.translation.get_translation(
            "configure_game_panel_name")).grid(row=0, column=0)

        self.players_entry_string_variable = [
            tkinter.tix.StringVar(),
            tkinter.tix.StringVar()
        ]

        self.players_entry_string_variable[0].set(
            self.ui.translation.get_translation("default_player_name").format("1"))
        self.players_entry_string_variable[1].set(
            self.ui.translation.get_translation("default_player_name").format("2")
        )

        self.players_entry = [tkinter.tix.Entry(self.players_name_frame[0],
                                                textvariable=self.players_entry_string_variable[0]),
                              tkinter.tix.Entry(self.players_name_frame[1],
                                                textvariable=self.players_entry_string_variable[1])]

        self.players_entry_string_variable[0].trace_add(
            "write", lambda x, y, z: self.name_string_var_trace_write()
        )

        self.players_entry_string_variable[1].trace_add(
            "write", lambda x, y, z: self.name_string_var_trace_write()
        )

        self.players_entry[0].grid(row=0, column=1)
        self.players_entry[1].grid(row=0, column=1)

        self.players_settings_scrolled_window = [
            tkinter.tix.ScrolledWindow(self, relief=tkinter.tix.SUNKEN, borderwidth=3),
            tkinter.tix.ScrolledWindow(self, relief=tkinter.tix.SUNKEN, borderwidth=3)
        ]

        self.players_settings_scrolled_window[0].grid(row=1, column=0, sticky=tkinter.tix.NSEW, pady=10, padx=5)
        self.players_settings_scrolled_window[1].grid(row=1, column=1, sticky=tkinter.tix.NSEW, pady=10, padx=5)

        self.players_settings_window = [self.players_settings_scrolled_window[0].window,
                                        self.players_settings_scrolled_window[1].window]

        for i in range(0, 2):
            self.players_settings_window[i].grid_columnconfigure(0, weight=1)

        self.player_ai_choose_var = [tkinter.tix.IntVar(),
                                     tkinter.tix.IntVar()]

        self.player_ai_choose = [
            tkinter.tix.Checkbutton(
                self.players_settings_window[0],
                text=self.ui.translation.get_translation("configure_game_panel_artificial_intelligence"),
                variable=self.player_ai_choose_var[0],
                command=self.check_button_ai_command),
            tkinter.tix.Checkbutton(
                self.players_settings_window[1],
                text=self.ui.translation.get_translation("configure_game_panel_artificial_intelligence"),
                variable=self.player_ai_choose_var[1],
                command=self.check_button_ai_command)
        ]
        self.player_ai_choose[0].grid(row=0, column=0, sticky=tkinter.tix.W)
        self.player_ai_choose[1].grid(row=0, column=0, sticky=tkinter.tix.W)

        self.players_tokens = [
            TokenStyle.TokenStyle(random.randint(0, TokenStyle.NUMBER_COLOR - 1)),
            TokenStyle.TokenStyle(random.randint(0, TokenStyle.NUMBER_COLOR - 1))
        ]

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

        self.players_text_choose = [
            tkinter.tix.Label(
                self.players_settings_window[0],
                text=self.ui.translation.get_translation("configure_game_panel_choose_tokens")),
            tkinter.tix.Label(
                self.players_settings_window[1],
                text=self.ui.translation.get_translation("configure_game_panel_choose_tokens"))]

        self.players_text_choose[0].grid(row=2, column=0, sticky=tkinter.tix.W)
        self.players_text_choose[1].grid(row=2, column=0, sticky=tkinter.tix.W)

        self.token_choose_frame = [tkinter.tix.Frame(self.players_settings_window[0]),
                                   tkinter.tix.Frame(self.players_settings_window[1])]

        self.token_choose_frame[0].grid(row=3, column=0, sticky=tkinter.tix.NSEW)
        self.token_choose_frame[1].grid(row=3, column=0, sticky=tkinter.tix.NSEW)

        self.button_token_choose_per_line = 0
        self.button_token_choose_per_line_last = 0  # to remove column configure

        self.token_choose_buttons = [[], []]
        for index in range(0, TokenStyle.NUMBER_COLOR):
            self.token_choose_buttons[0].append(tkinter.tix.Button(self.token_choose_frame[0],
                                                                   image=self.ui.image_getter.save_token_icons[
                                                                       TokenState.Player_1]
                                                                   [TokenStyle.TokenStyle(index)],
                                                                   command=lambda _index=index:
                                                                   self.button_change_token_command(
                                                                       _index, TokenState.Player_1)))

            self.token_choose_buttons[1].append(tkinter.tix.Button(self.token_choose_frame[1],
                                                                   image=self.ui.image_getter.save_token_icons[
                                                                       TokenState.Player_2]
                                                                   [TokenStyle.TokenStyle(index)],
                                                                   command=lambda _index=index:
                                                                   self.button_change_token_command(
                                                                       _index, TokenState.Player_2)))

        tkinter.tix.Label(self,
                          text=self.ui.translation.get_translation("configure_game_panel_difficulty_text")
                          ).grid(row=2, column=0, columnspan=2)

        self.difficultly_choose_scrolled_window = tkinter.tix.ScrolledWindow(self)
        self.difficultly_choose_scrolled_window.grid(row=3, column=0, columnspan=2, sticky=tkinter.tix.SE + tkinter.W,
                                                     pady=5)

        self.difficultly_choose_window = self.difficultly_choose_scrolled_window.window

        self.difficulty_selected_button = 0

        self.difficulty_buttons = [
            tkinter.tix.Button(
                self.difficultly_choose_window,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_very_easy")
                    .format(self.ui.preference.get_preference(PREFERENCE_DIFFICULTY_LEVEl)[0]),
                command=lambda: self.button_difficulty_command(0)),
            tkinter.tix.Button(
                self.difficultly_choose_window,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_easy")
                    .format(self.ui.preference.get_preference(PREFERENCE_DIFFICULTY_LEVEl)[1]),
                command=lambda: self.button_difficulty_command(1)),
            tkinter.tix.Button(
                self.difficultly_choose_window,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_normal")
                    .format(self.ui.preference.get_preference(PREFERENCE_DIFFICULTY_LEVEl)[2]),
                command=lambda: self.button_difficulty_command(2)),
            tkinter.tix.Button(
                self.difficultly_choose_window,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_little_hard")
                    .format(self.ui.preference.get_preference(PREFERENCE_DIFFICULTY_LEVEl)[3]),
                command=lambda: self.button_difficulty_command(3)),
            tkinter.tix.Button(
                self.difficultly_choose_window,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_hard")
                    .format(self.ui.preference.get_preference(PREFERENCE_DIFFICULTY_LEVEl)[4]),
                command=lambda: self.button_difficulty_command(4)),
            tkinter.tix.Button(
                self.difficultly_choose_window,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_very_hard")
                    .format(self.ui.preference.get_preference(PREFERENCE_DIFFICULTY_LEVEl)[5]),
                command=lambda: self.button_difficulty_command(5))
        ]

        for i in range(0, len(self.difficulty_buttons)):
            self.difficulty_buttons[i].configure(borderwidth=3, relief=tkinter.tix.RIDGE)
            self.difficulty_buttons[i].grid(row=0, column=i, sticky=tkinter.tix.NSEW)
            self.difficultly_choose_window.columnconfigure(i, weight=1)

        self.button_difficulty_command(DEFAULT_BUTTON_DIFFICULTY_SELECT)

        self.button_main_menu = tkinter.tix.Button(
            self,
            text=self.ui.translation.get_translation("back"),
            command=self.button_main_menu_command)
        self.button_main_menu.grid(row=4, column=0, sticky=tkinter.tix.NSEW)

        self.button_play = tkinter.tix.Button(
            self,
            text=self.ui.translation.get_translation("play"),
            command=self.button_play_command)
        self.button_play.grid(row=4, column=1, sticky=tkinter.tix.NSEW)

        self.import_last_game_setting()
        self.check_button_ai_command()

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
        super().on_resize(event)

    def recreate_tokens_buttons(self):
        """
        Recreate tokens buttons
        :return: None
        """
        self.button_token_choose_per_line_last = self.button_token_choose_per_line
        self.button_token_choose_per_line = max(
            min(
                int(self.players_settings_window[0].winfo_width() / (ImageGetter.TOKEN_ICON_SIZE + TOKEN_MARGIN)),
                TokenStyle.NUMBER_COLOR,
            ),
            1
        )

        for i in range(0, max(self.button_token_choose_per_line, self.button_token_choose_per_line_last)):
            if i < self.button_token_choose_per_line:
                self.token_choose_frame[0].columnconfigure(i, weight=1)
                self.token_choose_frame[1].columnconfigure(i, weight=1)
            else:
                self.token_choose_frame[0].columnconfigure(i, weight=0)
                self.token_choose_frame[1].columnconfigure(i, weight=0)

        for index in range(0, TokenStyle.NUMBER_COLOR):
            if index % self.button_token_choose_per_line == 0:
                self.token_choose_frame[0].rowconfigure(int(index / self.button_token_choose_per_line), pad=3)
                self.token_choose_frame[1].rowconfigure(int(index / self.button_token_choose_per_line), pad=3)

            self.token_choose_buttons[0][index].grid(row=int(index / self.button_token_choose_per_line),
                                                     column=index % self.button_token_choose_per_line)

            self.token_choose_buttons[1][index].grid(row=int(index / self.button_token_choose_per_line),
                                                     column=index % self.button_token_choose_per_line)

    def import_last_game_setting(self):
        """
        Import the preferences set in the last game
        :return: None
        """
        if self.ui.preference.temporary_preference_exist(TEMPORARY_PREFERENCES_PLAYERS_NAMES):
            self.players_entry_string_variable[0].set(
                self.ui.preference.get_temporary_preference(TEMPORARY_PREFERENCES_PLAYERS_NAMES)[0])

            self.players_entry_string_variable[1].set(
                self.ui.preference.get_temporary_preference(TEMPORARY_PREFERENCES_PLAYERS_NAMES)[1])

        if self.ui.preference.temporary_preference_exist(TEMPORARY_PREFERENCES_PLAYERS_AI):
            self.player_ai_choose_var[0].set(
                self.ui.preference.get_temporary_preference(TEMPORARY_PREFERENCES_PLAYERS_AI)[0])

            self.player_ai_choose_var[1].set(
                self.ui.preference.get_temporary_preference(TEMPORARY_PREFERENCES_PLAYERS_AI)[1])

        if self.ui.preference.temporary_preference_exist(TEMPORARY_PREFERENCES_PLAYERS_TOKENS):
            tokens = self.ui.preference.get_temporary_preference(TEMPORARY_PREFERENCES_PLAYERS_TOKENS)

            for i in range(0, 2):
                self.players_tokens[i] = tokens[i]

                self.players_tokens_images[i] = \
                    self.ui.image_getter.save_token_photos[TokenState(i + 1)][self.players_tokens[i]]

                self.players_tokens_labels[i].config(image=self.players_tokens_images[i])

        if self.ui.preference.temporary_preference_exist(TEMPORARY_PREFERENCES_DIFFICULTY):
            self.difficulty_selected_button = self.ui.preference.get_temporary_preference(
                TEMPORARY_PREFERENCES_DIFFICULTY)

    def export_last_game_settings(self):
        """
        Export setting to save the preference of the last game
        :return: None
        """

        players_names = (self.players_entry_string_variable[0].get().strip(),
                         self.players_entry_string_variable[1].get().strip())

        self.ui.preference.set_temporary_preference(TEMPORARY_PREFERENCES_PLAYERS_NAMES, players_names)

        players_ai = [self.player_ai_choose_var[0].get(),
                      self.player_ai_choose_var[1].get()]

        self.ui.preference.set_temporary_preference(TEMPORARY_PREFERENCES_PLAYERS_AI, players_ai)

        self.ui.preference.set_temporary_preference(TEMPORARY_PREFERENCES_PLAYERS_TOKENS, self.players_tokens)

        self.ui.preference.set_temporary_preference(TEMPORARY_PREFERENCES_DIFFICULTY, self.difficulty_selected_button)

    def button_play_command(self):
        """
        The command of the play button
        :return: None
        """
        self.export_last_game_settings()

        if len(self.players_entry_string_variable[0].get().strip()) < 3:
            tkinter.messagebox.showerror(
                self.ui.translation.get_translation("configure_game_panel_dialog_name_blank_title"),
                self.ui.translation.get_translation("configure_game_panel_dialog_name_blank_message").format("1")
            )
            return None

        if len(self.players_entry_string_variable[1].get().strip()) < 3:
            tkinter.messagebox.showerror(
                self.ui.translation.get_translation("configure_game_panel_dialog_name_blank_title"),
                self.ui.translation.get_translation("configure_game_panel_dialog_name_blank_message").format("2")
            )
            return None

        if self.players_entry_string_variable[0].get().strip() == self.players_entry_string_variable[1].get().strip():
            tkinter.messagebox.showerror(
                self.ui.translation.get_translation("configure_game_panel_dialog_same_name_title"),
                self.ui.translation.get_translation("configure_game_panel_dialog_same_name_message")
            )
            return None

        if self.players_tokens[0] == self.players_tokens[1]:
            if not tkinter.messagebox.askokcancel(
                    self.ui.translation.get_translation("configure_game_panel_dialog_same_token_title"),
                    self.ui.translation.get_translation("configure_game_panel_dialog_same_token_message")):
                return None

        game = Game.Game()
        game.current_turn = random.choice((TokenState.Player_1, TokenState.Player_2))

        if self.player_ai_choose_var[0].get():
            player_1 = AIPlayer.AIPlayer(self.ui.preference.get_preference(PREFERENCE_DIFFICULTY_LEVEl
                                                                           )[self.difficulty_selected_button],
                                         game, TokenState.Player_1,
                                         self.players_tokens[0], self.players_entry_string_variable[0].get().strip())
        else:
            player_1 = Player.Player(TokenState.Player_1, self.players_tokens[0],
                                     self.players_entry_string_variable[0].get().strip())

        if self.player_ai_choose_var[1].get():
            player_2 = AIPlayer.AIPlayer(self.ui.preference.get_preference(PREFERENCE_DIFFICULTY_LEVEl
                                                                           )[self.difficulty_selected_button],
                                         game, TokenState.Player_2,
                                         self.players_tokens[1], self.players_entry_string_variable[1].get().strip())
        else:
            player_2 = Player.Player(TokenState.Player_2, self.players_tokens[1],
                                     self.players_entry_string_variable[1].get().strip())

        self.ui.change_panel(GamePanel.GamePanel,
                             player_1=player_1,
                             player_2=player_2,
                             game=game, delay=self.ui.preference.get_preference(PREFERENCE_DELAY))

    def name_string_var_trace_write(self):
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
        if len(self.players_entry_string_variable[0].get().strip()) >= 3 and \
                self.players_entry_string_variable[0].get().strip() == \
                self.players_entry_string_variable[1].get().strip():
            self.players_entry[0].configure(fg="#ee8f2f")
            self.players_entry[1].configure(fg="#ee8f2f")

    def button_main_menu_command(self):
        """
        The command of the main menu
        :return: None
        """
        self.export_last_game_settings()
        self.ui.change_panel(MainMenuPanel.MainMenuPanel)

    def button_change_token_command(self, index, player):
        """
        When a button to change token is clicked
        :param player: the player which have this token
        :param index: the index of the button
        :return: None
        """
        player_index = (1, 0)[player == TokenState.Player_1]

        self.players_tokens[player_index] = TokenStyle.TokenStyle(index)

        self.players_tokens_images[player_index] = \
            self.ui.image_getter.save_token_photos[player][self.players_tokens[player_index]]

        self.players_tokens_labels[player_index].config(image=self.players_tokens_images[player_index])

    def button_difficulty_command(self, index):
        """
        When a button of difficulty is clicked
        :param index: the index of the button
        :return: None
        """
        self.difficulty_buttons[self.difficulty_selected_button].config(
            relief=tkinter.tix.RIDGE, activebackground="#ebebeb", borderwidth=3,
            background=self.cget("background"))

        self.difficulty_selected_button = index

        font_color = "#2ca02c"

        if index == 0:
            font_color = "#37c837"
        elif index == 1:
            font_color = "#2ca02c"
        elif index == 2:
            font_color = "#a0a02c"
        elif index == 3:
            font_color = "#a0662c"
        elif index == 4:
            font_color = "#a0492c"
        elif index == 5:
            font_color = "#a02c2c"

        if self.player_ai_choose_var[0].get() or self.player_ai_choose_var[1].get():
            self.difficulty_buttons[self.difficulty_selected_button].config(
                relief=tkinter.tix.RAISED, activebackground=font_color, background=font_color, borderwidth=3)

    def check_button_ai_command(self):
        """
        When a button which is use for choose ai is click
        :return: None
        """

        if self.player_ai_choose_var[0].get() or self.player_ai_choose_var[1].get():
            for i in range(0, len(self.difficulty_buttons)):
                self.difficulty_buttons[i].config(state=tkinter.tix.NORMAL)

        else:
            for i in range(0, len(self.difficulty_buttons)):
                self.difficulty_buttons[i].config(state=tkinter.tix.DISABLED)

        self.button_difficulty_command(self.difficulty_selected_button)

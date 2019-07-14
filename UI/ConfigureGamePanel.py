import random
import tkinter.messagebox
import tkinter.tix

import AIPlayer
import Game
import Player
from TokenState import TokenState
from UI import Panel, GamePanel, MainMenuPanel, TokenStyle

PLAYERS_NAMES_PREFERENCES = "last_game_player_names_game"
PLAYERS_TOKENS_PREFERENCES = "last_game_player_tokens_game"
PLAYERS_AI_PREFERENCES = "last_game_ai_game"
DIFFICULTY_PREFERENCES = "last_game_difficulty"


class ConfigureGamePanel(Panel.Panel):
    """
    The panel which configure the game, chose skin...
    """

    def __init__(self, master, ui):
        super().__init__(master, ui)
        self.ui.image_getter.resize_tokens_images(150)

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
        self.players_entry[0].grid(row=0, column=1)
        self.players_entry[1].grid(row=0, column=1)

        self.players_settings_frame = [tkinter.tix.Frame(self, relief=tkinter.tix.SUNKEN, borderwidth=3),
                                       tkinter.tix.Frame(self, relief=tkinter.tix.SUNKEN, borderwidth=3)]

        self.players_settings_frame[0].grid(row=1, column=0, sticky=tkinter.tix.NSEW, pady=10, padx=5)
        self.players_settings_frame[1].grid(row=1, column=1, sticky=tkinter.tix.NSEW, pady=10, padx=5)

        for i in range(0, 2):
            self.players_settings_frame[i].grid_columnconfigure(1, weight=1)

        self.player_ai_choose_var = [tkinter.tix.IntVar(),
                                     tkinter.tix.IntVar()]

        self.player_ai_choose = [
            tkinter.tix.Checkbutton(
                self.players_settings_frame[0],
                text=self.ui.translation.get_translation("configure_game_panel_artificial_intelligence"),
                variable=self.player_ai_choose_var[0],
                command=self.check_button_ai_command),
            tkinter.tix.Checkbutton(
                self.players_settings_frame[1],
                text=self.ui.translation.get_translation("configure_game_panel_artificial_intelligence"),
                variable=self.player_ai_choose_var[1],
                command=self.check_button_ai_command)
        ]
        self.player_ai_choose[0].grid(row=0, column=0, columnspan=2, sticky=tkinter.tix.W)
        self.player_ai_choose[1].grid(row=0, column=0, columnspan=2, sticky=tkinter.tix.W)

        self.players_text_choose = [
            tkinter.tix.Label(
                self.players_settings_frame[0],
                text=self.ui.translation.get_translation("configure_game_panel_choose_tokens")),
            tkinter.tix.Label(
                self.players_settings_frame[1],
                text=self.ui.translation.get_translation("configure_game_panel_choose_tokens"))]

        self.players_text_choose[0].grid(row=1, column=0, sticky=tkinter.tix.W)
        self.players_text_choose[1].grid(row=1, column=0, sticky=tkinter.tix.W)

        self.players_tokens = [
            TokenStyle.TokenColor(random.randint(0, TokenStyle.NUMBER_COLOR - 1)),
            TokenStyle.TokenColor(random.randint(0, TokenStyle.NUMBER_COLOR - 1))
        ]

        self.players_tokens_images = [
            self.ui.image_getter.save_token_photos[TokenState.Player_1][self.players_tokens[0]],
            self.ui.image_getter.save_token_photos[TokenState.Player_2][self.players_tokens[1]]
        ]

        self.players_tokens_buttons = [
            tkinter.tix.Button(self.players_settings_frame[0], image=self.players_tokens_images[0],
                               command=lambda: self.button_change_token_command(TokenState.Player_1)),
            tkinter.tix.Button(self.players_settings_frame[1], image=self.players_tokens_images[1],
                               command=lambda: self.button_change_token_command(TokenState.Player_2))
        ]

        self.players_tokens_buttons[0].grid(row=1, column=1, sticky=tkinter.tix.NSEW)
        self.players_tokens_buttons[1].grid(row=1, column=1, sticky=tkinter.tix.NSEW)

        self.difficultly_choose_frame = tkinter.tix.Frame(self)
        self.difficultly_choose_frame.grid(row=2, column=0, columnspan=2, sticky=tkinter.tix.SE + tkinter.W,
                                           pady=10)

        self.difficulty_selected_button = 0

        self.difficulty_buttons = [
            tkinter.tix.Button(
                self.difficultly_choose_frame,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_very_easy"),
                command=lambda: self.button_difficulty_command(0)),
            tkinter.tix.Button(
                self.difficultly_choose_frame,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_easy"),
                command=lambda: self.button_difficulty_command(1)),
            tkinter.tix.Button(
                self.difficultly_choose_frame,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_normal"),
                command=lambda: self.button_difficulty_command(2)),
            tkinter.tix.Button(
                self.difficultly_choose_frame,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_little_hard"),
                command=lambda: self.button_difficulty_command(3)),
            tkinter.tix.Button(
                self.difficultly_choose_frame,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_hard"),
                command=lambda: self.button_difficulty_command(4)),
            tkinter.tix.Button(
                self.difficultly_choose_frame,
                text=self.ui.translation.get_translation("configure_game_panel_difficulty_very_hard"),
                command=lambda: self.button_difficulty_command(5))
        ]

        tkinter.tix.Label(self.difficultly_choose_frame,
                          text=self.ui.translation.get_translation("configure_game_panel_difficulty_text")
                          ).grid(
            row=0, column=0, columnspan=len(self.difficulty_buttons))

        for i in range(0, len(self.difficulty_buttons)):
            self.difficulty_buttons[i].grid(row=1, column=i, sticky=tkinter.tix.NSEW)
            self.difficultly_choose_frame.columnconfigure(i, weight=1)

        self.button_difficulty_command(2)

        self.button_main_menu = tkinter.tix.Button(
            self,
            text=self.ui.translation.get_translation("back"),
            command=self.button_main_menu_command)
        self.button_main_menu.grid(row=3, column=0, sticky=tkinter.tix.NSEW)

        self.button_play = tkinter.tix.Button(
            self,
            text=self.ui.translation.get_translation("play"),
            command=self.button_play_command)
        self.button_play.grid(row=3, column=1, sticky=tkinter.tix.NSEW)

        self.import_last_game_setting()
        self.check_button_ai_command()

    def import_last_game_setting(self):
        """
        Import the preferences set in the last game
        :return: None
        """
        if self.ui.preference.temporary_preference_exist(PLAYERS_NAMES_PREFERENCES):
            self.players_entry_string_variable[0].set(
                self.ui.preference.get_temporary_preference(PLAYERS_NAMES_PREFERENCES)[0])

            self.players_entry_string_variable[1].set(
                self.ui.preference.get_temporary_preference(PLAYERS_NAMES_PREFERENCES)[1])

        if self.ui.preference.temporary_preference_exist(PLAYERS_AI_PREFERENCES):
            self.player_ai_choose_var[0].set(
                self.ui.preference.get_temporary_preference(PLAYERS_AI_PREFERENCES)[0])

            self.player_ai_choose_var[1].set(
                self.ui.preference.get_temporary_preference(PLAYERS_AI_PREFERENCES)[1])

        if self.ui.preference.temporary_preference_exist(PLAYERS_TOKENS_PREFERENCES):
            tokens = self.ui.preference.get_temporary_preference(PLAYERS_TOKENS_PREFERENCES)

            for i in range(0, 2):
                self.players_tokens[i] = tokens[i]

                self.players_tokens_images[i] = \
                    self.ui.image_getter.save_token_photos[TokenState(i + 1)][self.players_tokens[i]]

                self.players_tokens_buttons[i].config(image=self.players_tokens_images[i])

        if self.ui.preference.temporary_preference_exist(DIFFICULTY_PREFERENCES):
            self.difficulty_selected_button = self.ui.preference.get_temporary_preference(DIFFICULTY_PREFERENCES)

    def export_last_game_settings(self):
        """
        Export setting to save the preference of the last game
        :return: None
        """

        players_names = (self.players_entry_string_variable[0].get(),
                         self.players_entry_string_variable[1].get())

        self.ui.preference.set_temporary_preference(PLAYERS_NAMES_PREFERENCES, players_names)

        players_ai = [self.player_ai_choose_var[0].get(),
                      self.player_ai_choose_var[1].get()]

        self.ui.preference.set_temporary_preference(PLAYERS_AI_PREFERENCES, players_ai)

        self.ui.preference.set_temporary_preference(PLAYERS_TOKENS_PREFERENCES, self.players_tokens)

        self.ui.preference.set_temporary_preference(DIFFICULTY_PREFERENCES, self.difficulty_selected_button)

    def button_play_command(self):
        """
        The command of the play button
        :return: None
        """
        self.export_last_game_settings()
        if self.players_tokens[0] == self.players_tokens[1]:
            if not tkinter.messagebox.askokcancel(
                    self.ui.translation.get_translation("configure_game_panel_dialog_same_token_title"),
                    self.ui.translation.get_translation("configure_game_panel_dialog_same_token_message")):
                return None

        if self.difficulty_selected_button == 5:
            if not tkinter.messagebox.askokcancel(
                    self.ui.translation.get_translation("configure_game_panel_dialog_very_hard_title"),
                    self.ui.translation.get_translation("configure_game_panel_dialog_very_hard_message")):
                return None

        game = Game.Game()

        if self.player_ai_choose_var[0].get():
            player_1 = AIPlayer.AIPlayer(self.difficulty_selected_button + 1, game, TokenState.Player_1,
                                         self.players_tokens[0], self.players_entry_string_variable[0].get())
        else:
            player_1 = Player.Player(TokenState.Player_1, self.players_tokens[0],
                                     self.players_entry_string_variable[0].get())

        if self.player_ai_choose_var[1].get():
            player_2 = AIPlayer.AIPlayer(self.difficulty_selected_button + 1, game, TokenState.Player_2,
                                         self.players_tokens[1], self.players_entry_string_variable[1].get())
        else:
            player_2 = Player.Player(TokenState.Player_2, self.players_tokens[1],
                                     self.players_entry_string_variable[1].get())

        self.ui.change_panel(GamePanel.GamePanel,
                             player_1=player_1,
                             player_2=player_2,
                             game=game)

    def button_main_menu_command(self):
        """
        The command of the main menu
        :return: None
        """
        self.export_last_game_settings()
        self.ui.change_panel(MainMenuPanel.MainMenuPanel)

    def button_change_token_command(self, player):
        """
        When a button to change token is clicked
        :param player: the player which have this token
        :return: None
        """

        player_index = (1, 0)[player == TokenState.Player_1]

        color_index = self.players_tokens[player_index].value + 1

        if color_index >= TokenStyle.NUMBER_COLOR:
            color_index = 0

        self.players_tokens[player_index] = TokenStyle.TokenColor(color_index)

        self.players_tokens_images[player_index] = \
            self.ui.image_getter.save_token_photos[player][self.players_tokens[player_index]]

        self.players_tokens_buttons[player_index].config(image=self.players_tokens_images[player_index])

    def button_difficulty_command(self, index):
        """
        When a button of difficulty is clicked
        :param index: the index of the button
        :return: None
        """
        self.difficulty_buttons[self.difficulty_selected_button].config(
            relief=tkinter.tix.GROOVE, activebackground="#ebebeb", borderwidth=1,
            background=self.cget("background"), pady=4)

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
                relief=tkinter.tix.SUNKEN, activebackground=font_color, background=font_color, borderwidth=5, pady=0,
                padx=0)

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

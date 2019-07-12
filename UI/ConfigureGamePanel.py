import random
import tkinter.tix

from TokenState import TokenState
from UI import Panel, GamePanel, MainMenuPanel
from UI import TokenColor


class ConfigureGamePanel(Panel.Panel):
    """
    The panel which configure the game, chose skin...
    """

    def __init__(self, master, ui, solo_mode=False):
        super().__init__(master, ui)
        self.solo_mode = solo_mode

        self.ui.image_getter.resize_tokens_images(150)

        for i in range(0, 2):
            self.grid_columnconfigure(i, weight=1)

        for i in range(1, 2):
            self.grid_rowconfigure(i, weight=1)

        self.players_label = [tkinter.tix.Label(self, text="Player 1:"),
                              tkinter.tix.Label(self, text="Player 2:")]
        self.players_label[0].grid(row=0, column=0)
        self.players_label[1].grid(row=0, column=1)

        self.players_settings_frame = [tkinter.tix.Frame(self),
                                       tkinter.tix.Frame(self)]

        self.players_settings_frame[0].grid(row=1, column=0, sticky=tkinter.tix.N, pady=10)
        self.players_settings_frame[1].grid(row=1, column=1, sticky=tkinter.tix.N, pady=10)

        for i in range(0, 2):
            self.players_settings_frame[i].grid_columnconfigure(0)

        self.players_text_choose = [tkinter.tix.Label(self.players_settings_frame[0], text="Choose you token:"),
                                    tkinter.tix.Label(self.players_settings_frame[1], text="Choose you token:")]

        self.players_text_choose[0].grid(row=0, column=0, sticky=tkinter.tix.W)
        self.players_text_choose[1].grid(row=0, column=0, sticky=tkinter.tix.W)

        self.players_tokens = [
            TokenColor.TokenColor(random.randint(0, TokenColor.NUMBER_COLOR - 1)),
            TokenColor.TokenColor(random.randint(0, TokenColor.NUMBER_COLOR - 1))
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

        self.players_tokens_buttons[0].grid(row=1, column=0, sticky=tkinter.tix.NSEW)
        self.players_tokens_buttons[1].grid(row=1, column=0, sticky=tkinter.tix.NSEW)

        self.button_main_menu = tkinter.tix.Button(self, text="Back", command=self.button_main_menu_command)
        self.button_main_menu.grid(row=2, column=0, sticky=tkinter.tix.NSEW)

        self.button_play = tkinter.tix.Button(self, text="Play", command=self.button_play_command)
        self.button_play.grid(row=2, column=1, sticky=tkinter.tix.NSEW)

    def button_play_command(self):
        """
        The command of the play button
        :return: None
        """
        self.ui.change_panel(GamePanel.GamePanel, solo_mode=self.solo_mode,
                             token_player_1=self.players_tokens[0],
                             token_player_2=self.players_tokens[1])

    def button_main_menu_command(self):
        """
        The command of the main menu
        :return: None
        """
        self.ui.change_panel(MainMenuPanel.MainMenuPanel)

    def button_change_token_command(self, player):
        """
        When a button to change token is clicked
        :param player: the player which have this token
        :return: None
        """

        player_index = (1, 0)[player == TokenState.Player_1]

        color_index = self.players_tokens[player_index].value + 1

        if color_index >= TokenColor.NUMBER_COLOR:
            color_index = 0

        self.players_tokens[player_index] = TokenColor.TokenColor(color_index)

        self.players_tokens_images[player_index] = \
            self.ui.image_getter.save_token_photos[player][self.players_tokens[player_index]]

        self.players_tokens_buttons[player_index].config(image=self.players_tokens_images[player_index])

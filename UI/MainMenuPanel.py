import tkinter.tix

from UI import Panel, GamePanel


class MainMenuPanel(Panel.Panel):
    """
    The main menu
    """

    def __init__(self, master, ui):
        """
        Constructor
        :param master:
        :param ui:
        """
        super().__init__(master, ui)

        for i in range(0, 1):
            self.grid_columnconfigure(i, weight=1)

        for i in range(0, 1):
            self.grid_rowconfigure(i, weight=1)

        self.text_title = tkinter.tix.Label(self, text="Power 4", font=("Arial Bold", 50))
        self.text_title.grid(row=0, column=0, sticky=tkinter.tix.NSEW)

        self.button_play_local_solo_player = tkinter.tix.Button(
            self, text="Play 1 player", command=self.button_play_local_solo_player_command, height=2,)
        self.button_play_local_solo_player.grid(row=1, column=0, sticky=tkinter.tix.NSEW)

        self.button_play_local_multi_players = tkinter.tix.Button(
            self, text="Play 2 players", command=self.button_play_local_multi_players_command, height=2)
        self.button_play_local_multi_players.grid(row=2, column=0, sticky=tkinter.tix.NSEW)

        self.button_quit = tkinter.tix.Button(self, text="Quit", command=self.button_quit_command)
        self.button_quit.grid(row=3, column=0, sticky=tkinter.tix.NSEW)

    def button_play_local_solo_player_command(self):
        """
        The command of the solo player button
        :return: None
        """
        self.ui.change_panel(GamePanel.GamePanel, solo_mode=True)

    def button_play_local_multi_players_command(self):
        """
        The command of the multi players button
        :return: None
        """
        self.ui.change_panel(GamePanel.GamePanel)

    def button_quit_command(self):
        """
        The command of the quit button
        :return: None
        """
        self.ui.destroy()

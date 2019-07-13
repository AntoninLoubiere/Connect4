import tkinter.tix

from UI import Panel, ConfigureGamePanel


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

        self.text_title = tkinter.tix.Label(self, text="Connect 4", font=("Arial Bold", 50))
        self.text_title.grid(row=0, column=0, sticky=tkinter.tix.NSEW)

        self.button_play_local_play = tkinter.tix.Button(
            self, text="Play", command=self.button_play_local_play_command, height=1, font=("Arial Bold", 20))
        self.button_play_local_play.grid(row=1, column=0, sticky=tkinter.tix.NSEW)

        self.button_quit = tkinter.tix.Button(self, text="Quit", command=self.button_quit_command)
        self.button_quit.grid(row=2, column=0, sticky=tkinter.tix.NSEW)

    def button_play_local_play_command(self):
        """
        The command of the multi players button
        :return: None
        """
        self.ui.change_panel(ConfigureGamePanel.ConfigureGamePanel)

    def button_quit_command(self):
        """
        The command of the quit button
        :return: None
        """
        self.ui.destroy()

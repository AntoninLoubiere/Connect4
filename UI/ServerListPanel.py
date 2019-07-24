import re
import tkinter.tix
import tkinter.messagebox

from UI import Panel, ServerGameConfigurationPanel
from main.Client import Client
from main.Server import Server

IP_REGEX = r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." + \
           r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." + \
           r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." + \
           r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"


class ServerListPanel(Panel.Panel):
    """
    The server list panel
    """

    def __init__(self, master, ui):
        """
        Constructor
        """
        super().__init__(master, ui)

        for r in range(0, 1):
            self.grid_rowconfigure(r, weight=1)

        for c in range(0, 2):
            self.grid_columnconfigure(c, weight=1)

        self.manual_connexion_frame = tkinter.tix.Frame(self)
        self.manual_connexion_frame.grid(row=1, column=0, columnspan=2, sticky=tkinter.tix.NSEW)

        for c in range(0, 5):
            self.manual_connexion_frame.columnconfigure(c, weight=1)

        tkinter.tix.Label(
            self.manual_connexion_frame,
            text=self.ui.translation.get_translation("server_list_manual_connexion_frame_text")
        ).grid(row=0, column=0, sticky=tkinter.tix.NSEW)

        tkinter.tix.Label(
            self.manual_connexion_frame,
            text=self.ui.translation.get_translation("server_list_manual_connexion_frame_host")
        ).grid(row=0, column=1, sticky=tkinter.tix.E)

        self.manual_connexion_host_string_var = tkinter.tix.StringVar()
        self.manual_connexion_host_string_var.set(Server.get_ip())
        self.manual_connexion_host_entry = tkinter.tix.Entry(self.manual_connexion_frame,
                                                             textvariable=self.manual_connexion_host_string_var)
        self.manual_connexion_host_entry.grid(row=0, column=2, sticky=tkinter.tix.NSEW)

        tkinter.tix.Label(
            self.manual_connexion_frame,
            text=self.ui.translation.get_translation("server_list_manual_connexion_frame_port")
        ).grid(row=0, column=3, sticky=tkinter.tix.E)

        self.manual_connexion_port = tkinter.tix.Spinbox(self.manual_connexion_frame, from_=3000, to=4000, wrap=True)
        self.manual_connexion_port.grid(row=0, column=4, sticky=tkinter.tix.NSEW)

        self.play_button = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("play"), state=tkinter.tix.DISABLED
        )
        self.play_button.grid(row=2, column=0, sticky=tkinter.tix.NSEW)

        self.manual_connexion_button = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("server_list_manual_connexion"),
            command=self.manual_connexion_button_command
        )
        self.manual_connexion_button.grid(row=2, column=1, sticky=tkinter.tix.NSEW)

        self.back_button = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("back"), command=self.button_back_command)

        self.back_button.grid(row=3, column=0, sticky=tkinter.tix.NSEW)

        self.create_game_button = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("server_list_create_game"),
            command=self.button_create_game_command)

        self.create_game_button.grid(row=3, column=1, sticky=tkinter.tix.NSEW)

    def button_back_command(self):
        """
        Return to the main menu
        :return: None
        """
        from UI import MainMenuPanel

        self.ui.change_panel(MainMenuPanel.MainMenuPanel)

    def button_create_game_command(self):
        """
        Whe the button create game is clicked
        :return: None
        """
        self.ui.change_panel(ServerGameConfigurationPanel.ServerGameConfigurationPanel, create_game=True)

    def manual_connexion_button_command(self):
        """
        When the button manual connexion is clicked
        :return: None
        """
        host = re.compile(IP_REGEX).match(self.manual_connexion_host_string_var.get())
        port = self.manual_connexion_port.get()

        if host:
            host = host[0]
        else:
            tkinter.messagebox.showerror(
                self.ui.translation.get_translation("server_list_dialog_host_error_title"),
                self.ui.translation.get_translation("server_list_dialog_host_error_message").format(Server.get_ip())
            )
            return None

        try:
            port = int(port)
        except ValueError:
            tkinter.messagebox.showerror(
                self.ui.translation.get_translation("server_configuration_dialog_port_error_title"),
                self.ui.translation.get_translation("server_configuration_dialog_port_error_message")
            )
            return None

        if not (3000 <= port <= 4000):
            tkinter.messagebox.showerror(
                self.ui.translation.get_translation("server_configuration_dialog_port_error_title"),
                self.ui.translation.get_translation("server_configuration_dialog_port_error_message")
            )
            return None

        if Server.exist(host, port):
            self.ui.client = Client(host, port)
            if self.ui.client.connect():
                self.ui.change_panel(ServerGameConfigurationPanel.ServerGameConfigurationPanel, create_game=False)
        else:
            tkinter.messagebox.showerror(
                self.ui.translation.get_translation("server_list_dialog_unreachable_title"),
                self.ui.translation.get_translation("server_list_dialog_unreachable_message")
            )
            return None

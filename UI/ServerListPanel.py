import socket
import tkinter.messagebox
import tkinter.tix

from UI import Panel, ServerGameConfigurationPanel
from main.Client import Client
from main.Server import Server, ServerScanner


class ServerListPanel(Panel.Panel):
    """
    The server list panel
    """

    def __init__(self, master, ui):
        """
        Constructor
        """
        super().__init__(master, ui)

        for r in range(1, 2):
            self.grid_rowconfigure(r, weight=1)

        for c in range(0, 2):
            self.grid_columnconfigure(c, weight=1)

        tkinter.tix.Label(
            self,
            text=self.ui.translation.get_translation("server_list_server_detected")
        ).grid(row=0, column=0, sticky=tkinter.tix.W)

        self.scrolled_window_server_detected = tkinter.tix.ScrolledWindow(self)
        self.scrolled_window_server_detected.grid(row=1, column=0, columnspan=2, sticky=tkinter.tix.NSEW)

        self.window_server_detected = self.scrolled_window_server_detected.window

        self.window_server_detected.grid_columnconfigure(0, weight=1)

        self.dict_server_detected = {}

        self.manual_connexion_frame = tkinter.tix.Frame(self)
        self.manual_connexion_frame.grid(row=2, column=0, columnspan=2, sticky=tkinter.tix.NSEW)

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

        self.manual_connexion_port = tkinter.tix.Spinbox(self.manual_connexion_frame, from_=3000, to=3020, wrap=True)
        self.manual_connexion_port.grid(row=0, column=4, sticky=tkinter.tix.NSEW)

        self.play_button = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("play"), state=tkinter.tix.DISABLED
        )
        self.play_button.grid(row=3, column=0, sticky=tkinter.tix.NSEW)

        self.manual_connexion_button = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("server_list_manual_connexion"),
            command=self.manual_connexion_button_command
        )
        self.manual_connexion_button.grid(row=3, column=1, sticky=tkinter.tix.NSEW)

        self.back_button = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("back"), command=self.button_back_command)

        self.back_button.grid(row=4, column=0, sticky=tkinter.tix.NSEW)

        self.create_game_button = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("server_list_create_game"),
            command=self.button_create_game_command)

        self.create_game_button.grid(row=4, column=1, sticky=tkinter.tix.NSEW)

        self.server_scanner = ServerScanner.ServerScanner(list_update_function=self.server_scanner_server_detection)

    def on_create_finish(self):
        """
        When the windows in pack see in panel class
        :return: None
        """
        self.server_scanner.start()

    def server_scanner_server_detection(self, add_remove, host_port):
        """
        When the server scanner detect a server
        :param add_remove: if is an add or a remove of the server
        :param host_port: the address of the server
        :return: None
        """
        if add_remove == ServerScanner.SERVER_ADD:
            self.dict_server_detected[host_port] = tkinter.tix.Frame(self.window_server_detected,
                                                                     relief=tkinter.tix.SUNKEN,
                                                                     borderwidth=2)
            self.dict_server_detected[host_port].grid_columnconfigure(0, weight=1)
            tkinter.tix.Label(
                self.dict_server_detected[host_port],
                text=self.ui.translation.get_translation("server_list_server_frame_text").format(
                    *host_port, socket.getfqdn(host_port[0])
                )
            ).grid(row=0, column=0, sticky=tkinter.tix.W)

            tkinter.tix.Button(
                self.dict_server_detected[host_port],
                text=self.ui.translation.get_translation("play").format(*host_port),
                command=lambda address=host_port: self.button_play_server_command(address)
            ).grid(row=0, column=1, sticky=tkinter.tix.E)
            self.update_list_server_detected()
        else:
            if host_port in self.dict_server_detected:
                self.dict_server_detected[host_port].destroy()
                del self.dict_server_detected[host_port]
                self.update_list_server_detected()

    def update_list_server_detected(self):
        """
        Update the list of server detected
        :return: None
        """
        sorted_list = sorted(self.dict_server_detected, key=lambda item: item[0][0])

        for i, host_port in enumerate(sorted_list):
            self.dict_server_detected[host_port].grid(row=i, column=0, sticky=tkinter.tix.NSEW)

    def button_play_server_command(self, host_port):
        """
        When the button to play with a server
        :param host_port: host and port of the server
        :return: None
        """
        if Server.exist(host_port[0], host_port[1]):
            self.ui.client = Client(host_port[0], host_port[1])
            if self.ui.client.connect():
                self.ui.change_panel(ServerGameConfigurationPanel.ServerGameConfigurationPanel, create_game=False)
        else:
            self.server_scanner_server_detection(ServerScanner.SERVER_REMOVE, host_port)

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
        try:
            host = socket.gethostbyname(self.manual_connexion_host_string_var.get())
        except socket.gaierror:
            tkinter.messagebox.showerror(
                self.ui.translation.get_translation("server_list_dialog_host_error_title"),
                self.ui.translation.get_translation("server_list_dialog_host_error_message").format(Server.get_ip())
            )
            return None
        port = self.manual_connexion_port.get()

        try:
            port = int(port)
        except ValueError:
            tkinter.messagebox.showerror(
                self.ui.translation.get_translation("server_configuration_dialog_port_error_title"),
                self.ui.translation.get_translation("server_configuration_dialog_port_error_message")
            )
            return None

        if not (3000 <= port <= 3020):
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
            return

    def destroy(self):
        """
        When the window is destroy
        :return: None
        """
        self.server_scanner.list_update_function = lambda add_remove, host_port: None
        self.server_scanner.stop_scan = True
        super().destroy()

import tkinter.tix

from main import Preferences, Translation
from UI import ImageGetter
from main.Server import Server

WIDTH = 720
HEIGHT = 620

MIN_WIDTH = 420
MIN_HEIGHT = 300


class UI(tkinter.tix.Tk):
    """
    The UI
    """

    def __init__(self):
        """
        Constructor
        """

        super().__init__()
        self.current_panel = None
        self.is_alive = True

        self.server = Server(max_clients_connected=1)
        self.client = None

        self.preference = Preferences.Preferences(default_preferences=Preferences.DEFAULT_PREFERENCES)
        self.translation = Translation.Translation(self.preference)
        self.image_getter = ImageGetter.ImageGetter(self.translation)
        # Configure
        self.title(self.translation.get_translation("connect_four"))
        # noinspection SpellCheckingInspection
        self.iconphoto(True, self.image_getter.logo_image)  # set the logo
        self.geometry("{}x{}".format(WIDTH, HEIGHT))
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def change_panel(self, new_panel, **kwargs):
        """
        Change the panel
        :param new_panel: the new panel
        :return: None
        """
        if self.current_panel is not None:
            self.current_panel.destroy()

        new_panel = new_panel(master=self, ui=self, **kwargs)

        self.current_panel = new_panel
        self.current_panel.pack(expand=True, fill=tkinter.tix.BOTH)
        self.update()
        self.current_panel.on_create_finish()

    def mainloop(self, n=0):
        self.is_alive = True
        super().mainloop(n)

    def destroy(self):
        self.is_alive = False

        if self.server.server_is_on:
            self.server.stop_server()

        if self.client is not None and self.client.connected:
            self.client.close_connection()

        super().destroy()

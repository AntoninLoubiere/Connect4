import tkinter.tix

import Preferences
import Translation
from UI import ImageGetter


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

        self.image_getter = ImageGetter.ImageGetter()
        self.preference = Preferences.Preferences()

        self.translation = Translation.Translation(self.preference)

        # Configure
        self.title(self.translation.get_translation("connect_four"))
        self.geometry("600x520")
        self.minsize(560, 300)
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

    def tick_update(self):
        """
        Tick update to current panel see panel class
        :return: None
        """

        if self.current_panel is not None:
            self.current_panel.tick_update()

    def mainloop(self, n=0):
        self.is_alive = True
        super().mainloop(n)

    def destroy(self):
        self.is_alive = False
        super().destroy()

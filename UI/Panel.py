import tkinter.tix


class Panel(tkinter.tix.Frame):
    """
    A panel to show in GUI
    """

    def __init__(self, master, ui):
        """
        Constructor
        :param master: The master to frame
        :param ui: link to UI
        """
        super().__init__(master)

        self.ui = ui

    def on_create_finish(self):
        """
        Call when the window is create and the size is OK
        :return: None
        """
        pass

    def tick_update(self):
        """
        When the program is update (especially for animation)
        :return: None
        """

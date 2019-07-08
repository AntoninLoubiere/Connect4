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

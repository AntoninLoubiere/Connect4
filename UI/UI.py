import tkinter.tix


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

        # Configure
        self.title("Power 4")
        self.geometry("600x520")

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
        self.current_panel.on_create_finish()


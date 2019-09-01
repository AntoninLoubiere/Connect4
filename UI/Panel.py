import tkinter.tix

from UI.UI import UI


class Panel(tkinter.tix.Frame):
    """
    A panel to show in GUI
    """
    def __init__(self, master, ui):
        """
        Constructor
        :param master: The master to frame
        :param ui: link to UI
        :type ui: UI
        """
        super().__init__(master)

        self.ui = ui
        self.ui.bind("<Configure>", self._resize_event)

        self.last_event = None
        self.resize_in_progress = None
        self.disable_resize_event = False

    def destroy(self):
        """
        When the window is destroy
        :return: None
        """
        self.ui.unbind("<Configure>")
        self.disable_resize_event = True
        super().destroy()

    def _resize_event(self, event):
        """
        When the window is resize PRIVATE FUNCTION
        :param event: the tkinter event
        :return: None
        """
        if self.disable_resize_event:
            return None

        if self.resize_in_progress:
            self.last_event = event

        else:
            self.resize_in_progress = True
            self.on_resize(event)

    def on_create_finish(self):
        """
        Call when the window is create and the size is OK
        :return: None
        """
        pass

    def on_resize(self, event):
        """
        When the window is resize
        :return: None
        """
        if self.last_event is None or self.disable_resize_event:
            self.resize_in_progress = False

        else:
            self.update_idletasks()
            new_event = self.last_event
            self.last_event = None
            self.on_resize(new_event)

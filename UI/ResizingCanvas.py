import tkinter.tix


class ResizingCanvas(tkinter.tix.Canvas):
    """
    A auto resizing canvas
    """

    def __init__(self, parent, window, on_resize_var=None, disable=False, **kwargs):
        """
        Constructor
        :param parent: the parent of the canvas
        :param window: the window
        :param disable: if the resize event is disable
        :param kwargs: Other params
        """
        tkinter.tix.Canvas.__init__(self, parent, **kwargs)
        window.bind("<Configure>", self.on_resize)
        self.window = window
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.on_resize_var = on_resize_var
        self.disable = disable

        self.last_event = None
        self.resize_in_progress = None

    def on_resize(self, event):
        """
        When the window is resize, resize the canvas
        :param event: the event
        :return: None
        """
        if self.disable:
            return None

        if self.resize_in_progress:
            self.last_event = event

        else:
            self.do_resize(event)

    def do_resize(self, event):
        """
        Do the resize
        :param event: the event
        :return: None
        """
        self.resize_in_progress = True

        # determine the ratio of old width/height to new width/height
        w_scale = float(event.width) / self.width
        h_scale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, w_scale, h_scale)

        if self.on_resize_var is not None:
            self.on_resize_var()

        if self.last_event is None:
            self.resize_in_progress = False

        else:
            new_event = self.last_event
            self.last_event = None
            self.do_resize(new_event)

    def remove_resizing(self):
        """
        Remove the auto resizing
        :return: None
        """
        self.window.unbind("<Configure>")

    def set_width(self, new_width):
        """
        Set the width
        :param new_width: the new width 
        :return: None
        """
        if new_width <= 0:
            new_width = 1
        self.width = new_width
        
    def set_height(self, new_height):
        """
        Set the height
        :param new_height: the new height 
        :return: None
        """
        if new_height <= 0:
            new_height = 1
        self.height = new_height

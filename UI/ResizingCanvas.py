import tkinter.tix


class ResizingCanvas(tkinter.tix.Canvas):
    """
    A auto resizing canvas
    """

    def __init__(self, parent, window, on_resize_var=None, **kwargs):
        """
        Constructor
        :param parent: the parent of the canvas
        :param window: the window
        :param kwargs: Other params
        """
        tkinter.tix.Canvas.__init__(self, parent, **kwargs)
        window.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.on_resize_var = on_resize_var

    def on_resize(self, event):
        """
        When the window is resize, resize the canvas
        :param event: the event
        :return: None
        """
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

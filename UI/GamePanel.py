from UI import Panel
import tkinter.tix
import Game


class GamePanel(Panel.Panel):
    """
    GamePanel is a panel for UI, is the UI for the game
    """

    def __init__(self, master, ui, **kwargs):
        """
        Constructor
        :param master: see Panel class
        :param ui: see Panel class
        """
        super().__init__(master, ui)

        self.grid_canvas = tkinter.tix.Canvas(self, width=600, height=400)
        self.grid_canvas.grid(row=1, column=0)

        self.game = Game.Game(**kwargs)

        self.draw_grid()

    def draw_grid(self):
        """
        Draw the grid in the canvas
        :return: None
        """

        space_between_column = self.grid_canvas.winfo_reqwidth() / float(self.game.grid_width)
        space_between_row = self.grid_canvas.winfo_reqheight() / float(self.game.grid_height)
        space_minimal = min(space_between_column, space_between_row)

        width_center = (self.grid_canvas.winfo_reqwidth() - space_minimal * self.game.grid_width) / 2
        height_center = (self.grid_canvas.winfo_reqheight() - space_minimal * self.game.grid_height) / 2

        print(space_between_row, space_between_column, space_minimal, width_center, height_center)
        for i in range(0, self.game.grid_width + 1):
            self.grid_canvas.create_line(space_minimal * i + width_center, height_center,
                                         space_minimal * i + width_center,
                                         self.grid_canvas.winfo_reqheight() - height_center)

        for i in range(0, self.game.grid_height + 1):
            self.grid_canvas.create_line(width_center, space_minimal * i + height_center,
                                         self.grid_canvas.winfo_reqwidth() - width_center, space_minimal * i +
                                         height_center)

import os
import TokenState
from UI import TokenColor
import tkinter.tix
from PIL import Image, ImageTk


class ImageGetter:
    """
    The getter and the saver of photos
    """

    def __init__(self, token_size=None):
        """
        Constructor
        """

        self.save_photos = {TokenState.TokenState.Player_1: {}, TokenState.TokenState.Player_2: {}}

        for i_player, player in enumerate(self.save_photos):
            for color in TokenColor.TokenColor:
                self.create_player_token_image(player, color, token_size, token_size)

    def create_player_token_image(self, player, color, size_x=None, size_y=None):
        """
        The player of the token
        :param player: The player of the token
        :param color: The color which he want
        :param size_x: the x resize
        :param size_y: the y resize
        :return: If is do TODO
        """

        file_path = os.getcwd() + "/UI/res/Token/" + player.name + "/" + color.name.lower() + ".png"

        img = Image.open(file_path, 'r')
        if size_x is not None and size_y is not None:
            img = img.resize((int(size_x), int(size_y)))

        self.save_photos[player][color] = ImageTk.PhotoImage(img)

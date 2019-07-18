import os

from PIL import Image, ImageTk

from main import TokenState
from UI import TokenStyle


def create_player_token_image(player, color, size_x=None, size_y=None):
    """
    The player of the token
    :param player: The player of the token
    :param color: The color which he want
    :param size_x: the x resize
    :param size_y: the y resize
    :return: Return image
    """

    file_path = os.getcwd() + "/UI/res/Token/" + player.name + "/" + color.name.lower() + ".png"

    img = Image.open(file_path, 'r')
    if size_x is not None and size_y is not None and size_x > 0 and size_y > 0:
        img = img.resize((int(size_x), int(size_y)), Image.ANTIALIAS)

    return img


class ImageGetter:
    """
    The getter and the saver of photos
    """

    def __init__(self, token_size=None):
        """
        Constructor
        """

        self.save_token_photos = {TokenState.TokenState.Player_1: {}, TokenState.TokenState.Player_2: {}}
        self.save_token_icons = {TokenState.TokenState.Player_1: {}, TokenState.TokenState.Player_2: {}}

        self.token_size = token_size

        for i_player, player in enumerate(self.save_token_photos):
            for color in TokenStyle.TokenColor:
                self.save_token_photos[player][color] = ImageTk.PhotoImage(create_player_token_image
                                                                           (player, color, token_size, token_size))

                self.save_token_icons[player][color] = ImageTk.PhotoImage(create_player_token_image
                                                                          (player, color, 30, 30))

    def resize_tokens_images(self, token_size):
        """
        Resize tokens images
        :return: None
        """

        if token_size == self.token_size:
            return None

        self.token_size = token_size

        for i_player, player in enumerate(self.save_token_photos):
            for color in TokenStyle.TokenColor:
                self.save_token_photos[player][color] = ImageTk.PhotoImage(
                    create_player_token_image(player, color, token_size, token_size))

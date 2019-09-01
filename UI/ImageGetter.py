import sys
import tkinter.messagebox

from PIL import Image, ImageTk

import main.Preferences
from UI import TokenStyle, NumberColor
from main import TokenState, DirectoryManager

WIN_TOKEN_BACKGROUND_RAPPORT_TOKEN = 1.3  # fraction size background / size token
ICON_SIZE = 30

TOKEN_ICON_SIZE = 30

NUMBER_SIZE_COEFFICIENT = 0.6
HEIGHT_NUMBER_COEFFICIENT = 1.5


class ImageGetter:
    """
    The getter and the saver of photos
    """

    def __init__(self, translation, token_size=None):
        """
        Constructor
        :param translation: A link ot translation file
        :param token_size: The size of tokens
        """
        self.translation = translation

        try:
            self.logo_image = ImageTk.PhotoImage(image=Image.open(DirectoryManager.get_path(
                (DirectoryManager.UI_RES_DIRECTORY, "connect4_logo.png"), add_current_directory=True))
            )
        except FileNotFoundError:
            print("WARNING: The logo isn't found !")

        try:
            self.default_token_image = ImageTk.PhotoImage(image=self.get_default_token_image(
                token_size, token_size))

            self.default_token_icon = ImageTk.PhotoImage(image=self.get_default_token_image(
                TOKEN_ICON_SIZE, TOKEN_ICON_SIZE))
        except FileNotFoundError:
            if translation.get_language(main.Preferences.DEFAULT_LANGUAGE) != -1:
                tkinter.messagebox.showerror(
                    translation.get_translation("no_default_image_dialog_title"),
                    translation.get_translation("no_default_image_dialog_message")
                )
            else:
                tkinter.messagebox.showerror(
                    "Default Image Not Found",
                    "The default image was not found! It mean also there aren't at least one token image! missing "
                    "Please check this problem by moving/downloading resources files in the directory UI -> res "
                )
            sys.exit(1)
        self.save_token_photos = {TokenState.TokenState.Player_1: {}, TokenState.TokenState.Player_2: {}}
        self.save_token_icons = {TokenState.TokenState.Player_1: {}, TokenState.TokenState.Player_2: {}}

        self.token_size = token_size

        for i_player, player in enumerate(self.save_token_photos):
            for color in TokenStyle.TokenStyle:
                try:
                    self.save_token_photos[player][color] = ImageTk.PhotoImage(self.create_player_token_image
                                                                               (player, color, token_size, token_size))

                    self.save_token_icons[player][color] = ImageTk.PhotoImage(self.create_player_token_image
                                                                              (player, color, TOKEN_ICON_SIZE,
                                                                               TOKEN_ICON_SIZE))
                except FileNotFoundError:
                    print("The token of the player {}, {}, isn't found !".format(player.value, color))
                    self.save_token_photos[player][color] = self.default_token_image
                    self.save_token_icons[player][color] = self.default_token_icon
                    continue

        if token_size is None:
            win_token_background_size = token_size
        else:
            win_token_background_size = token_size * WIN_TOKEN_BACKGROUND_RAPPORT_TOKEN

        self.win_token_background = ImageTk.PhotoImage(
            self.create_image(DirectoryManager.get_path((DirectoryManager.UI_RES_DIRECTORY, "Token",
                                                         "win_token_background.png"),
                                                        add_current_directory=True),
                              win_token_background_size,
                              win_token_background_size)
        )

        try:
            self.door_exit_icon = ImageTk.PhotoImage(
                self.create_image(DirectoryManager.get_path((DirectoryManager.UI_RES_DIRECTORY, "door_exit_icon.png"),
                                                            add_current_directory=True),
                                  ICON_SIZE,
                                  ICON_SIZE)
            )
        except FileNotFoundError:
            print("The file door_exit_icon was not found")

        self.numbers_list = {}
        number_width = None
        number_height = None
        if token_size is not None:
            number_width = token_size * NUMBER_SIZE_COEFFICIENT
            number_height = number_width * HEIGHT_NUMBER_COEFFICIENT

        for color in NumberColor.NumberColor:
            self.numbers_list[color] = {}
            for i in range(0, 10):
                self.numbers_list[color][i] = ImageTk.PhotoImage(self.create_number(color, i, number_width,
                                                                                    number_height))

    def resize_tokens_images(self, token_size):
        """
        Resize tokens images
        :return: None
        """

        if token_size == self.token_size:
            return None

        self.token_size = token_size

        for i_player, player in enumerate(self.save_token_photos):
            for color in TokenStyle.TokenStyle:
                self.save_token_photos[player][color] = ImageTk.PhotoImage(
                    self.create_player_token_image(player, color, token_size, token_size))

        if token_size is None:
            win_token_background_size = token_size
        else:
            win_token_background_size = token_size * WIN_TOKEN_BACKGROUND_RAPPORT_TOKEN

        self.win_token_background = ImageTk.PhotoImage(
            self.create_image(DirectoryManager.get_path((DirectoryManager.UI_RES_DIRECTORY, "Token",
                                                         "win_token_background.png"),
                                                        add_current_directory=True),
                              win_token_background_size,
                              win_token_background_size)
        )

        number_width = None
        number_height = None
        if token_size is not None:
            number_width = token_size * NUMBER_SIZE_COEFFICIENT
            number_height = number_width * HEIGHT_NUMBER_COEFFICIENT

        for color in NumberColor.NumberColor:
            self.numbers_list[color] = {}
            for i in range(0, 10):
                self.numbers_list[color][i] = ImageTk.PhotoImage(self.create_number(color, i, number_width,
                                                                                    number_height))

    def get_number_size(self):
        """
        Get number height
        :return: None
        """
        return self.token_size * NUMBER_SIZE_COEFFICIENT, self.token_size * NUMBER_SIZE_COEFFICIENT \
            * HEIGHT_NUMBER_COEFFICIENT

    @staticmethod
    def create_player_token_image(player, color, size_x=None, size_y=None):
        """
        The player of the token
        :param player: The player of the token
        :param color: The color which he want
        :param size_x: the x resize
        :param size_y: the y resize
        :return: Return image
        """

        file_path = DirectoryManager.get_path((DirectoryManager.UI_RES_DIRECTORY, "Token", player.name,
                                               color.name.lower() + ".png"), add_current_directory=True)

        return ImageGetter.create_image(file_path, size_x, size_y)

    @staticmethod
    def create_number(color, number, size_x=None, size_y=None):
        """
        The player of the token
        :param number: The number of the number
        :param color: The color which he want
        :param size_x: the x resize
        :param size_y: the y resize
        :return: Return image
        """

        file_path = DirectoryManager.get_path((DirectoryManager.UI_RES_DIRECTORY, "Numbers",
                                               "{}_{}.png".format(color.name.lower(), number)),
                                              add_current_directory=True)

        return ImageGetter.create_image(file_path, size_x, size_y)

    @staticmethod
    def create_image(path, size_x=None, size_y=None):
        """
        Create an image
        :param path: the path of the image
        :param size_x: the size (x) of the image
        :param size_y: the size (y) of the image
        :return: Return the image
        """
        img = Image.open(path, 'r')

        if size_x is not None and size_y is not None and size_x > 0 and size_y > 0:
            img = img.resize((int(size_x), int(size_y)), Image.ANTIALIAS)

        return img

    @staticmethod
    def get_default_token_image(size_x=None, size_y=None):
        """
        Get the default token image
        :param size_x: The size x of the token
        :param size_y: The size y of the token
        :return: An image
        """
        file_path = DirectoryManager.get_path((DirectoryManager.UI_RES_DIRECTORY, "Token", "default_token.png"),
                                              add_current_directory=True)

        return ImageGetter.create_image(file_path, size_x, size_y)

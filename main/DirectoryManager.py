import os
import sys

UI_RES_DIRECTORY = "UI" + os.sep + "res"


def get_path(list_folder, add_current_directory=False):
    """
    Transform a list of folder into a path
    :param add_current_directory: if add to path the current directory
    :param list_folder: The list of folder
    :return: The path from the list of folder
    """
    if add_current_directory:
        if getattr(sys, 'frozen', False):
            # noinspection PyUnresolvedReferences,PyProtectedMember
            path = sys._MEIPASS
        else:
            path = (os.getcwd())
        return os.sep.join((path, *list_folder))
    else:
        return os.sep.join(list_folder)

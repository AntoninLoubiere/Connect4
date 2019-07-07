"""
Project: Power 4
By: Antonin LOUBIERE (github.com/AntoninLoubiere)

Version: 0.1

Language: Python 3.7
License: GNU Public License v3.0 (In file "LICENSE.md")
Created: Sunday, July 7, 2019
"""
from Game import Game
from UI.UI import UI


def main():
    """
    Main method
    :return: None
    """

    game = Game()

    ui = UI()
    ui.mainloop()

    game.start_in_console()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
"""
Project: Power 4
By: Antonin LOUBIERE (github.com/AntoninLoubiere)

Version: 0.1

Language: Python 3.7
License: GNU Public License v3.0 (In file "LICENSE.md")
Created: Sunday, July 7, 2019
"""
from main.TickUpdater import TickUpdater
from UI.MainMenuPanel import MainMenuPanel
from UI.UI import UI


def main():
    """
    Main method
    :return: None
    """

    ui = UI()
    ui.change_panel(MainMenuPanel)

    tick_updater = TickUpdater(ui)
    tick_updater.start()

    ui.mainloop()


if __name__ == '__main__':
    main()

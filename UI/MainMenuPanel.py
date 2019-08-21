import tkinter.tix
import tkinter.ttk

from UI import Panel, ConfigureGamePanel, ServerListPanel, PreferencePanel


class MainMenuPanel(Panel.Panel):
    """
    The main menu
    """

    def __init__(self, master, ui):
        """
        Constructor
        :param master:
        :param ui:
        """
        super().__init__(master, ui)

        for i in range(0, 1):
            self.grid_columnconfigure(i, weight=1)

        for i in range(0, 1):
            self.grid_rowconfigure(i, weight=1)

        self.text_title = tkinter.tix.Label(self, text=self.ui.translation.get_translation("connect_four"),
                                            font=("Arial Bold", 50))
        self.text_title.grid(row=0, column=0, columnspan=2, sticky=tkinter.tix.NSEW)

        self.button_play_local = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("play_local"), command=self.button_play_local_command,
            height=1, font=("Arial Bold", 20))
        self.button_play_local.grid(row=1, column=0, columnspan=2, sticky=tkinter.tix.NSEW)

        self.button_play_online = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("play_online"), height=1, font=("Arial Bold", 20),
            command=self.button_play_online_command
        )

        self.button_play_online.grid(row=2, column=0, columnspan=2, sticky=tkinter.tix.NSEW)

        self.button_settings = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("settings"), height=1, font=("Arial Bold", 16),
            command=self.button_settings_command
        )
        self.button_settings.grid(row=3, column=0, columnspan=2, sticky=tkinter.tix.NSEW)

        self.button_quit = tkinter.tix.Button(self, text=self.ui.translation.get_translation("quit"),
                                              command=self.button_quit_command)
        self.button_quit.grid(row=4, column=0, sticky=tkinter.tix.NSEW)

        self.language_combo_box_values = []
        for language in self.ui.translation.list_translations:
            self.language_combo_box_values.append(language[1])

        self.language_combo_box = tkinter.ttk.Combobox(self, values=self.language_combo_box_values,
                                                       state='readonly')
        self.language_combo_box.current(self.ui.translation.current_language)
        self.language_combo_box.grid(row=4, column=1, sticky=tkinter.tix.NSEW)
        self.language_combo_box.bind("<<ComboboxSelected>>", lambda event: self.language_combobox_on_selected())

    def update_text(self):
        """
        Update the text in all widget
        :return:
        """
        self.text_title.configure(text=self.ui.translation.get_translation("connect_four"))
        self.button_play_local.configure(text=self.ui.translation.get_translation("play_local"))
        self.button_play_online.configure(text=self.ui.translation.get_translation("play_online"))
        self.button_quit.configure(text=self.ui.translation.get_translation("quit"))
        self.button_settings.configure(text=self.ui.translation.get_translation("settings"))

    def button_play_local_command(self):
        """
        The command of the multi players button
        :return: None
        """
        self.ui.change_panel(ConfigureGamePanel.ConfigureGamePanel)

    def button_play_online_command(self):
        """
        The command of the online button
        :return: None
        """
        self.ui.change_panel(ServerListPanel.ServerListPanel)

    def button_quit_command(self):
        """
        The command of the quit button
        :return: None
        """
        self.ui.destroy()

    def button_settings_command(self):
        """
        The command of the settings button
        :return: None
        """
        self.ui.change_panel(PreferencePanel.PreferencePanel)

    def language_combobox_on_selected(self):
        """
        When the combobox is selected
        :return: None
        """
        self.language_combo_box.selection_clear()

        self.ui.translation.set_current_language(self.language_combo_box.current())

        self.update_text()

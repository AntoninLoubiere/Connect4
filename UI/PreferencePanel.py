import tkinter.tix
import tkinter.ttk
import tkinter.messagebox

from UI import Panel
from main import Preferences

SCROLLBAR_SETTINGS_WIDTH = 16

NUMBER_DIFFICULTY_BUTTONS = 6
DIFFICULTY_BUTTONS_TEXT_KEY = [
    "preference_difficulty_very_easy",
    "preference_difficulty_easy",
    "preference_difficulty_normal",
    "preference_difficulty_little_hard",
    "preference_difficulty_hard",
    "preference_difficulty_very_hard",
]


class PreferencePanel(Panel.Panel):
    """
    The preference panel
    """

    def __init__(self, master, ui):
        """
        Constructor
        """
        super().__init__(master, ui)

        self.list_text_settings = []
        self.list_text_fill_line = []

        for i in range(0, 3):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(0, weight=1)

        self.scrolled_window = tkinter.tix.ScrolledWindow(self, scrollbar=tkinter.tix.Y)
        self.scrolled_window.grid(row=0, column=0, columnspan=3, sticky=tkinter.tix.NSEW)

        self.window_settings = self.scrolled_window.window

        self.window_settings.columnconfigure(0, weight=1)
        self.window_settings.columnconfigure(1, pad=2)
        self.window_settings.columnconfigure(2, pad=2)

        # SETTINGS FRAME

        self.settings_column_label = tkinter.tix.Label(
            self.window_settings, text=self.ui.translation.get_translation("preference_settings_column"),
            font=(None, 11, "bold")
        )
        self.settings_column_label.grid(row=0, column=0, sticky=tkinter.tix.NSEW)

        self.value_column_label = tkinter.tix.Label(
            self.window_settings, text=self.ui.translation.get_translation("preference_value_column"),
            font=(None, 11, "bold")
        )
        self.value_column_label.grid(row=0, column=1, sticky=tkinter.tix.NSEW)

        self.default_column_label = tkinter.tix.Label(
            self.window_settings, text=self.ui.translation.get_translation("preference_default_column"),
            font=(None, 11, "bold")
        )
        self.default_column_label.grid(row=0, column=2, sticky=tkinter.tix.NSEW)

        current_row = 0

        # !!! Section: Global !!!

        current_row += 1

        self.section_global_label = tkinter.tix.Label(
            self.window_settings, text=self.ui.translation.get_translation("preference_section_global"),
            font=(None, 15)
        )
        self.section_global_label.grid(row=current_row, column=0, columnspan=3, sticky=tkinter.tix.NSEW, pady=5)
        self.list_text_fill_line.append(self.section_global_label)

        # Language settings
        current_row += 1

        self.language_text = tkinter.tix.Label(
            self.window_settings, text=self.ui.translation.get_translation("preference_language"),
            justify=tkinter.tix.RIGHT
        )
        self.language_text.grid(row=current_row, column=0, sticky=tkinter.tix.E)
        self.list_text_settings.append(self.language_text)

        self.language_combo_box_values = []
        for language in self.ui.translation.list_translations:
            self.language_combo_box_values.append(language[1])

        self.language_combo_box = tkinter.ttk.Combobox(self.window_settings, values=self.language_combo_box_values,
                                                       state='readonly')
        self.language_combo_box.current(self.ui.translation.current_language)
        self.language_combo_box.grid(row=current_row, column=1, sticky=tkinter.tix.NSEW)
        self.language_combo_box.bind("<<ComboboxSelected>>", lambda event: self.language_combobox_on_selected())

        self.language_default_button = tkinter.tix.Button(
            self.window_settings,
            text=self.ui.translation.list_translations[
                self.ui.translation.get_language(Preferences.DEFAULT_LANGUAGE)
            ][1],
            command=lambda: self.set_default_preference_on_button_click(Preferences.PREFERENCE_CURRENT_LANGUAGE,
                                                                        Preferences.DEFAULT_LANGUAGE)
        )
        self.language_default_button.grid(row=current_row, column=2, sticky=tkinter.tix.NSEW)

        # Delay
        current_row += 1

        self.delay_text = tkinter.tix.Label(
            self.window_settings, text=self.ui.translation.get_translation("preference_delay"),
            justify=tkinter.tix.RIGHT
        )
        self.delay_text.grid(row=current_row, column=0, sticky=tkinter.tix.E)
        self.list_text_settings.append(self.delay_text)

        self.delay_spin_box_variable = tkinter.tix.StringVar()
        self.delay_spin_box_variable.set(str(self.ui.preference.get_preference(Preferences.PREFERENCE_DELAY)))

        self.delay_spin_box = tkinter.tix.Spinbox(
            self.window_settings, textvariable=self.delay_spin_box_variable,
            from_=Preferences.DELAY_MIN, to=Preferences.DELAY_MAX, increment=100
        )
        self.delay_spin_box.grid(row=current_row, column=1, sticky=tkinter.tix.NSEW)

        self.delay_spin_box_variable.trace_add("write", lambda x, y, z: self.on_spin_box_change(self.delay_spin_box))

        self.delay_default_text = tkinter.tix.Button(
            self.window_settings, text=Preferences.DEFAULT_DELAY,
            command=lambda: self.set_default_preference_on_button_click(Preferences.PREFERENCE_DELAY,
                                                                        Preferences.DEFAULT_DELAY)
        )
        self.delay_default_text.grid(row=current_row, column=2, sticky=tkinter.tix.NSEW)

        # Delay win
        current_row += 1

        self.delay_win_text = tkinter.tix.Label(
            self.window_settings, text=self.ui.translation.get_translation("preference_delay_win"),
            justify=tkinter.tix.RIGHT
        )
        self.delay_win_text.grid(row=current_row, column=0, sticky=tkinter.tix.E)
        self.list_text_settings.append(self.delay_win_text)

        self.delay_win_spin_box_variable = tkinter.tix.StringVar()
        self.delay_win_spin_box_variable.set(str(self.ui.preference.get_preference(Preferences.PREFERENCE_WIN_DELAY)))

        self.delay_win_spin_box = tkinter.tix.Spinbox(
            self.window_settings, textvariable=self.delay_win_spin_box_variable,
            from_=Preferences.DELAY_WIN_MIN, to=Preferences.DELAY_WIN_MAX, increment=100
        )
        self.delay_win_spin_box.grid(row=current_row, column=1, sticky=tkinter.tix.NSEW)

        self.delay_win_spin_box_variable.trace_add(
            "write",
            lambda x, y, z: self.on_spin_box_change(self.delay_win_spin_box)
        )

        self.delay_win_default_text = tkinter.tix.Button(
            self.window_settings, text=Preferences.DEFAULT_WIN_DELAY,
            command=lambda: self.set_default_preference_on_button_click(Preferences.PREFERENCE_WIN_DELAY,
                                                                        Preferences.DEFAULT_WIN_DELAY)
        )
        self.delay_win_default_text.grid(row=current_row, column=2, sticky=tkinter.tix.NSEW)

        # !!! Section: Difficulty !!!

        current_row += 1

        self.section_difficulty_label = tkinter.tix.Label(
            self.window_settings, text=self.ui.translation.get_translation("preference_section_difficulty"),
            font=(None, 15)
        )
        self.section_difficulty_label.grid(row=current_row, column=0, columnspan=3, sticky=tkinter.tix.NSEW, pady=5)
        self.list_text_fill_line.append(self.section_difficulty_label)

        current_row += 1
        self.difficulty_depth_text = tkinter.tix.Label(
            self.window_settings, text=self.ui.translation.get_translation("preference_difficulty_depth"),
            justify=tkinter.tix.LEFT
        )
        self.difficulty_depth_text.grid(row=current_row, column=0, columnspan=3, sticky=tkinter.tix.W)

        self.list_text_fill_line.append(self.difficulty_depth_text)

        self.difficulty_depth_settings_text_list = []
        self.difficulty_depth_variable_spin_box_list = []
        self.difficulty_depth_spin_box_list = []
        self.difficulty_depth_default_buttons_list = []

        for i in range(0, NUMBER_DIFFICULTY_BUTTONS):
            current_row += 1
            # Settings text
            self.difficulty_depth_settings_text_list.append(
                tkinter.tix.Label(
                    self.window_settings,
                    text=self.ui.translation.get_translation(DIFFICULTY_BUTTONS_TEXT_KEY[i]),
                    justify=tkinter.tix.RIGHT
                )
            )
            self.difficulty_depth_settings_text_list[i].grid(row=current_row, column=0, sticky=tkinter.tix.E)
            self.list_text_settings.append(self.difficulty_depth_settings_text_list[i])

            # Spin box

            self.difficulty_depth_variable_spin_box_list.append(tkinter.tix.StringVar())
            self.difficulty_depth_variable_spin_box_list[i].set(
                self.ui.preference.get_preference(Preferences.PREFERENCE_DIFFICULTY_DEPTH_LEVEL)[i]
            )

            self.difficulty_depth_spin_box_list.append(
                tkinter.tix.Spinbox(self.window_settings, textvariable=self.difficulty_depth_variable_spin_box_list[i],
                                    from_=Preferences.DIFFICULTY_LEVEL_DEPTH_MIN,
                                    to=Preferences.DIFFICULTY_LEVEL_DEPTH_MAX)
            )
            self.difficulty_depth_spin_box_list[i].grid(row=current_row, column=1, sticky=tkinter.tix.NSEW)

            self.difficulty_depth_variable_spin_box_list[i].trace_add(
                "write",
                lambda x, y, z, button_index=i: self.on_spin_box_change(
                    self.difficulty_depth_spin_box_list[button_index])
            )

            # Default value

            self.difficulty_depth_default_buttons_list.append(
                tkinter.tix.Button(
                    self.window_settings, text=str(Preferences.DEFAULT_DIFFICULTY_DEPTH_LEVEL[i]),
                    command=lambda button_id=i: self.set_default_preference_on_button_click(
                        Preferences.PREFERENCE_DIFFICULTY_DEPTH_LEVEL,
                        Preferences.DEFAULT_DIFFICULTY_DEPTH_LEVEL[button_id],
                        button_id
                    )
                )
            )
            self.difficulty_depth_default_buttons_list[i].grid(row=current_row, column=2, sticky=tkinter.tix.NSEW)

        current_row += 1
        self.difficulty_round_text = tkinter.tix.Label(
            self.window_settings, text=self.ui.translation.get_translation("preference_difficulty_round"),
            justify=tkinter.tix.LEFT
        )
        self.difficulty_round_text.grid(row=current_row, column=0, columnspan=3, sticky=tkinter.tix.W)

        self.list_text_fill_line.append(self.difficulty_round_text)

        self.difficulty_round_settings_text_list = []
        self.difficulty_round_variable_spin_box_list = []
        self.difficulty_round_spin_box_list = []
        self.difficulty_round_default_buttons_list = []

        for i in range(0, NUMBER_DIFFICULTY_BUTTONS):
            current_row += 1
            # Settings text
            self.difficulty_round_settings_text_list.append(
                tkinter.tix.Label(
                    self.window_settings,
                    text=self.ui.translation.get_translation(DIFFICULTY_BUTTONS_TEXT_KEY[i]),
                    justify=tkinter.tix.RIGHT
                )
            )
            self.difficulty_round_settings_text_list[i].grid(row=current_row, column=0, sticky=tkinter.tix.E)
            self.list_text_settings.append(self.difficulty_round_settings_text_list[i])

            # Spin box

            self.difficulty_round_variable_spin_box_list.append(tkinter.tix.StringVar())
            self.difficulty_round_variable_spin_box_list[i].set(
                self.ui.preference.get_preference(Preferences.PREFERENCE_DIFFICULTY_ROUND_LEVEL)[i]
            )

            self.difficulty_round_spin_box_list.append(
                tkinter.tix.Spinbox(self.window_settings, textvariable=self.difficulty_round_variable_spin_box_list[i],
                                    from_=Preferences.DIFFICULTY_LEVEL_ROUND_MIN,
                                    to=Preferences.DIFFICULTY_LEVEL_ROUND_MAX)
            )
            self.difficulty_round_spin_box_list[i].grid(row=current_row, column=1, sticky=tkinter.tix.NSEW)

            self.difficulty_round_variable_spin_box_list[i].trace_add(
                "write",
                lambda x, y, z, button_index=i: self.on_spin_box_change(
                    self.difficulty_round_spin_box_list[button_index])
            )

            # Default value

            self.difficulty_round_default_buttons_list.append(
                tkinter.tix.Button(
                    self.window_settings, text=str(Preferences.DEFAULT_DIFFICULTY_ROUND_LEVEL[i]),
                    command=lambda button_id=i: self.set_default_preference_on_button_click(
                        Preferences.PREFERENCE_DIFFICULTY_ROUND_LEVEL,
                        Preferences.DEFAULT_DIFFICULTY_ROUND_LEVEL[button_id],
                        button_id
                    )
                )
            )
            self.difficulty_round_default_buttons_list[i].grid(row=current_row, column=2, sticky=tkinter.tix.NSEW)

        # BUTTONS

        self.cancel_button = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("cancel"), command=self.cancel_button_command,
        )
        self.cancel_button.grid(row=1, column=0, sticky=tkinter.tix.NSEW)

        self.reset_button = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("preference_reset_preferences"),
            command=self.reset_button_command
        )
        self.reset_button.grid(row=1, column=1, sticky=tkinter.tix.NSEW)

        self.valid_button = tkinter.tix.Button(
            self, text=self.ui.translation.get_translation("valid"), command=self.valid_button_command
        )
        self.valid_button.grid(row=1, column=2, sticky=tkinter.tix.NSEW)

    def on_create_finish(self):
        """
        When the window is created
        :return: None
        """
        self.on_resize(None)

    def on_resize(self, event):
        """
        When the window is resize (See in Panel class)
        :param event: the tkinter event
        :return: None
        """
        self.set_wrap_settings_text()

        super().on_resize(event)

    def set_wrap_settings_text(self):
        """
        Set the wrap length to all settings text
        :return: None
        """
        text_width = self.winfo_width() - (self.value_column_label.winfo_width()
                                           + self.default_column_label.winfo_width() + SCROLLBAR_SETTINGS_WIDTH)

        for text in self.list_text_settings:
            text.configure(wraplength=text_width)

        for text in self.list_text_fill_line:
            text.configure(wraplength=self.winfo_width() - SCROLLBAR_SETTINGS_WIDTH)

    def cancel_button_command(self):
        """
        When the cancel button is clicked
        :return: None
        """
        self.ui.preference.load_preferences()
        self.ui.translation.reload_current_language()
        from UI.MainMenuPanel import MainMenuPanel
        self.ui.change_panel(MainMenuPanel)

    def reset_button_command(self):
        """
        When the reset button is clicked
        :return: None
        """
        self.ui.preference.reset_default_values_preference()
        self.reload_preference()

    def valid_button_command(self):
        """
        When the valid button is clicked
        :return: None
        """
        try:
            delay = int(self.delay_spin_box_variable.get())
            if Preferences.DELAY_MIN <= delay <= Preferences.DELAY_MAX:
                self.ui.preference.set_preference(Preferences.PREFERENCE_DELAY, delay)
            else:
                raise ValueError  # show the dialog
        except ValueError:
            tkinter.messagebox.showerror(
                self.ui.translation.get_translation("preference_error_input_title"),
                self.ui.translation.get_translation("preference_error_input_delay").format(
                    self.delay_spin_box_variable.get(), Preferences.DELAY_MIN, Preferences.DELAY_MAX
                )
            )
            return None

        try:
            delay = int(self.delay_win_spin_box_variable.get())
            if Preferences.DELAY_WIN_MIN <= delay <= Preferences.DELAY_WIN_MAX:
                self.ui.preference.set_preference(Preferences.PREFERENCE_WIN_DELAY, delay)
            else:
                raise ValueError  # show the dialog
        except ValueError:
            tkinter.messagebox.showerror(
                self.ui.translation.get_translation("preference_error_input_title"),
                self.ui.translation.get_translation("preference_error_input_win_delay").format(
                    self.delay_win_spin_box_variable.get(), Preferences.DELAY_WIN_MIN, Preferences.DELAY_WIN_MAX
                )
            )
            return None

        for i in range(0, NUMBER_DIFFICULTY_BUTTONS):
            try:
                difficulty_level = int(self.difficulty_depth_variable_spin_box_list[i].get())
                if Preferences.DIFFICULTY_LEVEL_DEPTH_MIN <= difficulty_level <= Preferences.DIFFICULTY_LEVEL_DEPTH_MAX:
                    self.ui.preference.get_preference(Preferences.PREFERENCE_DIFFICULTY_DEPTH_LEVEL)[i] \
                        = difficulty_level
                else:
                    raise ValueError  # show the dialog
            except ValueError:
                tkinter.messagebox.showerror(
                    self.ui.translation.get_translation("preference_error_input_title"),
                    self.ui.translation.get_translation("preference_error_input_difficulty").format(
                        self.ui.translation.get_translation(DIFFICULTY_BUTTONS_TEXT_KEY[i]),
                        self.difficulty_depth_variable_spin_box_list[i].get(),
                        Preferences.DIFFICULTY_LEVEL_DEPTH_MIN, Preferences.DIFFICULTY_LEVEL_DEPTH_MAX
                    )
                )
                return None
            
        for i in range(0, NUMBER_DIFFICULTY_BUTTONS):
            try:
                difficulty_level = int(self.difficulty_round_variable_spin_box_list[i].get())
                if Preferences.DIFFICULTY_LEVEL_ROUND_MIN <= difficulty_level <= Preferences.DIFFICULTY_LEVEL_ROUND_MAX:
                    self.ui.preference.get_preference(Preferences.PREFERENCE_DIFFICULTY_ROUND_LEVEL)[i] \
                        = difficulty_level
                else:
                    raise ValueError  # show the dialog
            except ValueError:
                tkinter.messagebox.showerror(
                    self.ui.translation.get_translation("preference_error_input_title"),
                    self.ui.translation.get_translation("preference_error_input_difficulty").format(
                        self.ui.translation.get_translation(DIFFICULTY_BUTTONS_TEXT_KEY[i]),
                        self.difficulty_round_variable_spin_box_list[i].get(),
                        Preferences.DIFFICULTY_LEVEL_ROUND_MIN, Preferences.DIFFICULTY_LEVEL_ROUND_MAX
                    )
                )
                return None

        self.ui.preference.save_preferences()

        from UI.MainMenuPanel import MainMenuPanel
        self.ui.change_panel(MainMenuPanel)

    def reload_preference(self, preference_id=None, list_id=None):
        """
        Reload preference because there is a change
        :return: None
        """
        if preference_id is None or preference_id == Preferences.PREFERENCE_CURRENT_LANGUAGE:
            self.ui.translation.reload_current_language()
            self.language_combo_box.current(self.ui.translation.current_language)

        if preference_id is None or preference_id == Preferences.PREFERENCE_DELAY:
            self.delay_spin_box_variable.set(self.ui.preference.get_preference(Preferences.PREFERENCE_DELAY))
        if preference_id is None or preference_id == Preferences.PREFERENCE_WIN_DELAY:
            self.delay_win_spin_box_variable.set(self.ui.preference.get_preference(Preferences.PREFERENCE_WIN_DELAY))

        if preference_id is None or preference_id == Preferences.PREFERENCE_DIFFICULTY_DEPTH_LEVEL:
            if list_id is None:
                for i, variable in enumerate(self.difficulty_depth_variable_spin_box_list):
                    variable.set(self.ui.preference.get_preference(Preferences.PREFERENCE_DIFFICULTY_DEPTH_LEVEL)[i])
            else:
                self.difficulty_depth_variable_spin_box_list[list_id]\
                    .set(self.ui.preference.get_preference(Preferences.PREFERENCE_DIFFICULTY_DEPTH_LEVEL)[list_id])

        if preference_id is None or preference_id == Preferences.PREFERENCE_DIFFICULTY_ROUND_LEVEL:
            if list_id is None:
                for i, variable in enumerate(self.difficulty_round_variable_spin_box_list):
                    variable.set(self.ui.preference.get_preference(Preferences.PREFERENCE_DIFFICULTY_ROUND_LEVEL)[i])
            else:
                self.difficulty_round_variable_spin_box_list[list_id]\
                    .set(self.ui.preference.get_preference(Preferences.PREFERENCE_DIFFICULTY_ROUND_LEVEL)[list_id])

    def reload_text(self):
        """
        Reload all text when the language is change
        :return: None
        """
        self.settings_column_label.configure(text=self.ui.translation.get_translation("preference_settings_column"))
        self.default_column_label.configure(text=self.ui.translation.get_translation("preference_default_column"))
        self.value_column_label.configure(text=self.ui.translation.get_translation("preference_value_column"))

        self.cancel_button.configure(text=self.ui.translation.get_translation("cancel"))
        self.reset_button.configure(text=self.ui.translation.get_translation("preference_reset_preferences"))
        self.valid_button.configure(text=self.ui.translation.get_translation("valid"))

        self.language_text.configure(text=self.ui.translation.get_translation("preference_language"))

        self.delay_text.configure(text=self.ui.translation.get_translation("preference_delay"))
        self.delay_win_text.configure(text=self.ui.translation.get_translation("preference_delay_win"))

        self.section_difficulty_label.configure(text=self.ui.translation.get_translation(
            "preference_section_difficulty"))
        self.difficulty_depth_text.configure(text=self.ui.translation.get_translation(
            "preference_difficulty_depth"))
        self.difficulty_round_text.configure(text=self.ui.translation.get_translation(
            "preference_difficulty_round"))

        for i, text in enumerate(self.difficulty_depth_settings_text_list):
            text.configure(text=self.ui.translation.get_translation(DIFFICULTY_BUTTONS_TEXT_KEY[i]))

        for i, text in enumerate(self.difficulty_round_settings_text_list):
            text.configure(text=self.ui.translation.get_translation(DIFFICULTY_BUTTONS_TEXT_KEY[i]))

    def language_combobox_on_selected(self):
        """
        When the combobox is selected
        :return: None
        """
        self.language_combo_box.selection_clear()

        self.ui.translation.set_current_language(self.language_combo_box.current(), save_preferences=False)

        self.reload_text()

    def set_default_preference_on_button_click(self, preference_id, preference_value, list_id=None):
        """
        When a button default is click, set the default preference and reload
        :param preference_id: the preference id
        :param preference_value: the preference value
        :param list_id: if the preference is a list, the id to set
        :return: None
        """
        if list_id is None:
            self.ui.preference.set_preference(preference_id, preference_value)
        else:
            self.ui.preference.get_preference(preference_id)[list_id] = preference_value

        self.reload_preference(preference_id, list_id)

        if preference_id == Preferences.PREFERENCE_CURRENT_LANGUAGE:
            self.reload_text()

    @staticmethod
    def on_spin_box_change(spin_box):
        """
        When the text of an spin box change, set the color red if the input is invalid
        :param spin_box: the spin_box
        :return: None
        """
        try:
            spin_box_value = int(spin_box.get())
            min_value = int(spin_box.cget("from"))
            max_value = int(spin_box.cget("to"))
            if min_value <= spin_box_value <= max_value:
                spin_box.configure(fg="black")
                return None
        except ValueError:
            pass
        spin_box.configure(fg="red")

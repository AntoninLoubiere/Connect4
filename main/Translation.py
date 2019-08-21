import glob
import os
import xml.dom.minidom

from main.Preferences import PREFERENCE_CURRENT_LANGUAGE, DEFAULT_LANGUAGE

TRANSLATION_FILES_PATH = "translations" + os.sep + "*.xml"
TRANSLATION_FILES_PATH_FORMAT = "translations" + os.sep + "{}.xml"


class Translation:
    """
    A translation file
    """

    def __init__(self, preference):
        """
        Constructor
        """
        self.current_language = -1
        self.list_translations = []
        self.update_dic_translation()
        self.preference = preference

        if self.preference.preference_exist(PREFERENCE_CURRENT_LANGUAGE):
            self.current_language = self.get_language(self.preference.get_preference(PREFERENCE_CURRENT_LANGUAGE))

        else:
            self.current_language = self.get_language(DEFAULT_LANGUAGE)

    def update_dic_translation(self) -> None:
        """
        Update list translations available
        :return: None
        """
        if self.current_language != -1:
            language_name = self.list_translations[self.current_language][0]
            self.current_language = -1
        else:
            language_name = ""

        self.list_translations = []

        for t in glob.glob(TRANSLATION_FILES_PATH):
            try:
                doc = xml.dom.minidom.parse(t)
                name = doc.getElementsByTagName("name")[0]
                self.list_translations.append((t.split(os.sep)[-1][:-4], name.firstChild.data))

                if t.split('/')[-1][:-4] == language_name:
                    self.current_language = len(self.list_translations) - 1
            except xml.dom.DOMException:
                pass

    def get_language(self, name) -> int:
        """
        Get a language by using his name
        :param name: the name of the language (EN_en, FR_fr...)
        :return: the id in the list
        """
        for i, t in enumerate(self.list_translations):
            if t[0] == name:
                return i

        return -1

    def get_translation(self, key, language_name=None) -> str:
        """
        Get a translation from a key
        :param language_name: The language name by default the current
        :param key: The key of the translation
        :return: the translation
        """

        if language_name is None:
            language_id = self.current_language
        else:
            language_id = self.get_language(language_name)

        try:
            translation_file_path = TRANSLATION_FILES_PATH_FORMAT.format(self.list_translations[language_id][0])

            doc = xml.dom.minidom.parse(translation_file_path)

            translations_list = doc.getElementsByTagName("language")[0].getElementsByTagName('translations')[0]. \
                getElementsByTagName("string")

            for translation in translations_list:
                if key == translation.getAttribute("name"):
                    return translation.firstChild.data

            else:
                if language_id == self.get_language(DEFAULT_LANGUAGE):
                    print("ERROR: The key, " + key + ", doesn't exist in the default file !")
                    return key

                print("WARNING: The key, " + key + ", doesn't exist in this language")
                return self.get_translation(key, DEFAULT_LANGUAGE)

        except FileNotFoundError:
            if language_id == self.get_language(DEFAULT_LANGUAGE):
                print("ERROR: The default file doesn't exist !")

                return key

            print("WARNING: The file of this language doesn't exist")

            return self.get_translation(key, DEFAULT_LANGUAGE)

        except IndexError:
            if language_id == self.get_language(DEFAULT_LANGUAGE):
                print("ERROR: The default file haven't a good format !")
                return key

            print("WARNING: The file of this language haven't a good format")

            return self.get_translation(key, DEFAULT_LANGUAGE)

    def set_current_language(self, new_current_language, save_preferences=True) -> None:
        """
        Set the current language
        :param save_preferences: If the language need to be save in the file
        :param new_current_language: the new value
        :return: None
        """
        self.current_language = new_current_language
        self.preference.set_preference(PREFERENCE_CURRENT_LANGUAGE, self.list_translations[self.current_language][0])
        if save_preferences:
            self.preference.save_preferences()

    def reload_current_language(self) -> None:
        """
        Reload the current language from preferences
        :return: None
        """
        self.current_language = self.get_language(self.preference.get_preference(PREFERENCE_CURRENT_LANGUAGE))

# External libraries
import subprocess
import sys
import json
import urllib.request

from bibtexparser.bparser import BibTexParser
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget
from time import asctime
from os import path, mkdir, rename

if sys.platform == "win32":
    from os import startfile

# Own stuff
from constants import ARTICLE_SAVE, SAVE_JSON, SIZE_ADD, SIZE_EXP, BASE_URL, SIZE_SET, SETTINGS_JSON, STANDARD_SETTINGS,\
    SIZE_CHA, NOTES_PATH, GENERAL
from core import article
from GUI import main_GUI, afk_GUI, add_GUI, export_GUI, settings_dialog, show_dialog, change_article_GUI


class control:

    # Basic initialization

    def __init__(self):

        # Init articles
        self.all_articles = self.help_load_articles()
        self.settings = self.help_load_settings()

        self.fp = None
        self.screensize = None
        self.currently_displayed = list(range(len(self.all_articles)))

        # Init afk control gui
        self.afk = afk_GUI(self.settings['SIZE_AFK'], self.settings['BUTTON_COLOR'], self.help_get_next_index())
        self.afk.button.dropped.connect(self.show_add)

        self.help_move_window(window=self.afk)
        self.main = None
        self.add = None
        self.export = None
        self.settings_dialog = None
        self.change_art = None

        # When the button is clicked the main window opens
        self.afk.button.clicked.connect(self.show_main)

    # Main functions

    def show_main(self):
        """Opens a main GUI and initializes all citations to be displayed
        :return: Nothing
        """
        # Initialize main GUI
        self.main = main_GUI(self.settings['SIZE_MAIN'],
                             self.settings['HIDE_EXPLAIN'],
                             self.settings['SHORTCUTS'])

        # Display all articles
        self.all_articles = self.help_load_articles()
        self.main_sort_and_display_articles()

        # Setting actions for main window
        self.main.citation_list.itemDoubleClicked.connect(self.main_open_pdf)
        self.main.show_exp.triggered.connect(self.show_export)
        self.main.combo.currentTextChanged.connect(self.main_sort_and_display_articles)

        self.main.quick_copy.triggered.connect(self.main_quick_copy)
        self.main.searchbar.textChanged.connect(self.main_search)
        self.main.add_button.clicked.connect(self.main_add_and)
        self.main.delete_article.triggered.connect(self.main_delete_row)
        self.main.show_settings.triggered.connect(self.show_settings)
        self.main.change_article.triggered.connect(self.main_show_change_article)
        self.main.close_all_windows.triggered.connect(self.main_close_all)
        self.main.open_notes.triggered.connect(self.main_open_notes)
        self.main.open_notes_folder.triggered.connect(self.help_open_notes_folder)
        self.main.open_arts_folder.triggered.connect(self.help_open_article_folder)

    def main_search(self):
        """Search for a string in all articles name, tags and BibTex citation. Creates a filtered list of articles and
        displays them.
        :return: Nothing
        """

        # Search text
        text = self.main.searchbar.text().lower().replace(' ', '|a|')

        s_text = text.split('|a|')

        res = []
        # Go through all articles and search for the text in the contents
        for ind, art in self.all_articles.items():
            add = {t: False for t in s_text}

            # Search for text in BibTex
            for key, value in art.get_bibtex().items():
                for t in s_text:
                    if t in value.lower():
                        add[t] = True

            # Search for text in name
            for t in s_text:
                if t in art.get_name().lower():
                    add[t] = True

            # Search for text in tags
            for el in art.get_tags():
                for t in s_text:
                    if t in el.lower():
                        add[t] = True

            if all(add.values()):
                res.append(ind)

        # Refresh displayed articles to only those with matching words
        self.currently_displayed = [int(r) for r in res]
        self.main_sort_and_display_articles()

    def main_delete_row(self):
        """Deletes a selected row. Refreshes the other rows by "pulling them up" so the index is always correct.
        :return: Nothing
        """

        # For now delete row works for only one row at a time
        selected_cit = None
        if self.main.citation_list.currentRow() >= 0:

            le = len(self.main.citation_list.selectedItems())

            # If number if selected rows is larger than 1
            if le > 6:
                for num in range(le // 6):
                    # Add all selected article indices to a list
                    pass
            else:

                # Only one article is selected, add index to list
                selected_cit = self.main.citation_list.selectedItems()[0].text()

            # Copy currently displayed articles
            curr = self.currently_displayed[:]
            self.currently_displayed = []

            # Go trough all articles
            for ind, article in self.all_articles.items():

                # If its the last article break
                if int(ind) == len(self.all_articles) - 1 and int(ind) != int(selected_cit):
                    if int(ind) in curr:
                        self.currently_displayed.append(int(ind) - 1)
                    break

                # If deleted article is the last one just break
                elif int(ind) == len(self.all_articles) - 1 and int(ind) == int(selected_cit):
                    break

                # If its the deleted article set its value to the next article
                elif int(ind) == int(selected_cit):
                    self.all_articles[ind] = self.all_articles[str(int(ind) + 1)]

                # If deleted article is before set article to last article
                elif int(ind) > int(selected_cit):
                    self.all_articles[ind] = self.all_articles[str(int(ind) + 1)]
                    if int(ind) in curr:
                        self.currently_displayed.append(int(ind) - 1)

                # If deleted article is still to come just add article
                elif int(ind) < int(selected_cit):
                    if int(ind) in curr:
                        self.currently_displayed.append(int(ind))

            # Delete duplicate article at the end
            del self.all_articles[str(self.help_get_next_index() - 1)]

            # Refresh display and save articles to JSON file
            self.main_sort_and_display_articles()
            self.help_dump_to_json()

    def main_add_and(self):
        """Add |a| to the searchbar to add multiple searches together.
        :return: Nothing
        """
        self.main.searchbar.setText(f'{self.main.searchbar.text()}|a|')

    def main_show_change_article(self):
        """Displays the article change menu.
        :return: Nothing
        """
        if self.main.citation_list.currentRow() >= 0:
            selected_art = self.main.citation_list.selectedItems()[0].text()
            art = self.all_articles[selected_art]
            self.change_art = change_article_GUI(SIZE_CHA, art.get_dict(), art.bibtex_to_string())

            self.change_art.accept.clicked.connect(lambda: self.main_change_citation(selected_art))
            self.change_art.decline.clicked.connect(self.change_art.close)

    def main_change_citation(self, ind):
        """Change the information of an article with a given id
        :param ind: string ID of the article
        :return: Nothing
        """
        dc = dict(self.all_articles)

        text = self.change_art.textedit.toPlainText()
        if text != '' and text[0] == "@" and text[-1] == "}":

            # Parameter for the new citation
            try:
                bibtex_dict = self.help_parse_latex(text)
            except:
                show_dialog('BibTex citations seems to be in a wrong format!', 'Error!')
                return

            label = self.change_art.nameedit.text()
            tags = self.change_art.tagsedit.text().split(',')
            old_fp = self.all_articles[ind].get_path()

            # Init of new citation
            cit = article(ind, label, old_fp, tags, asctime(), bibtex_dict, 0)
            if self.all_articles[ind].get_bibtex() == cit.get_bibtex():
                same_title = True
            else:
                same_title = False
            del self.all_articles[ind]

            if self.help_check_bibtex(bibtex_dict):
                if not same_title:
                    cit_title = cit.get_bibtex()["title"].lower().replace(" ", "_").replace(".", "").replace(",", "")
                    if len(cit_title) > 50:
                        cit_title = cit_title[:50]
                    title = f'{cit.get_index()}_{cit_title}.pdf'
                    cit.set_path(path.join(ARTICLE_SAVE, title))
                    if not path.exists(cit.get_path()):
                        rename(old_fp, cit.get_path())
                self.all_articles[ind] = cit
                self.help_dump_to_json()
                self.main_sort_and_display_articles()

            else:
                self.all_articles = dc
            self.change_art.close()

        else:
            show_dialog('BibTex citations seems to be in a wrong format!', 'Error!')

    def main_quick_copy(self):
        """Method to quickly copy the selected articles BibTex citation to the clipboard
        :return: Nothing
        """
        index = self.main.citation_list.currentRow()
        copy = '\n' + self.all_articles[str(index)].bibtex_to_string() + '\n'
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(copy, mode=cb.Clipboard)

    def main_sort_and_display_articles(self):
        """Uses the currently displayed articles and the sort settings as a basis to rearrange the table in user defined
        order.
        :return: Nothing
        """

        # Sorting the articles
        indices = self.currently_displayed[:]
        index = self.main.combo.currentIndex()

        # Sort by Index number
        if index == 0 or index == 1:
            indices = sorted(indices)

        # Sort by relevance score
        if index == 2 or index == 3:
            indices = sorted(indices, key=lambda x: self.all_articles[str(x)].get_relevance())

        # Turn list around
        if index == 1 or index == 3:
            indices = indices[::-1]

        # Generate display data for the indexed articles
        fin = []
        for ind in indices:
            fin.append(self.help_gen_show_name(ind))

        self.afk.update_num_citations(self.help_get_next_index())
        self.main.pop_list(fin)

    def main_open_pdf(self):
        """Open selected citation
        :return: Nothing
        """
        # Get selected citation
        selected_art = self.main.citation_list.selectedItems()[0].text()
        self.all_articles[selected_art].increase_relevance()
        self.help_dump_to_json()
        filepath = self.all_articles[selected_art].get_path()

        self.help_open_file(filepath)

    def main_close_all(self):
        """Terminates the whole program.
        :return: Nothing
        """
        app.closeAllWindows()

    def main_open_notes(self):
        """Open the notes for a specific article
        :return: Nothing
        """

        # If an article is selected
        if self.main.citation_list.currentRow() >= 0:

            # Get the article object and get the note_path of the object
            selected_art = self.all_articles[self.main.citation_list.selectedItems()[0].text()]
            note_path_sel = selected_art.get_note_path()

            # If the note path does not exist
            if note_path_sel == '':

                norm_path = selected_art.get_path()
                if self.settings['NOTES_FORMAT'] == "Text":
                    name = f'{norm_path.split(path.sep)[-1][:-4]}.txt'
                else:
                    name = f'{norm_path.split(path.sep)[-1][:-4]}.md'
                note_path_sel = path.join(NOTES_PATH, name)

                # Create new txt notes file in the NOTES directory

                with open(note_path_sel, 'w') as file:
                    file.write(' ')

                selected_art.set_note_path(note_path_sel)
                self.help_dump_to_json()

            if not path.exists(note_path_sel):
                selected_art.set_note_path('')
                show_dialog('The notes file was removed from the folder! and will be removed from the article file.'
                            , 'Error!')
                self.help_dump_to_json()

            else:
                self.help_open_file(note_path_sel)

    # Export functions

    def show_export(self):
        """Display export window and position it next to the main_GUI.
        :return: Nothing
        """
        # Initialize export GUI
        self.export = export_GUI(SIZE_EXP)

        # Reposition export GUI next to main GUI
        mainpos = self.main.pos()
        # Relocate the export window
        mainsize = self.main.geometry()
        if sys.platform == 'win32':
            self.export.relocate(mainpos.x() + mainsize.width(), mainpos.y())
        else:
            self.export.relocate(mainpos.x() + mainsize.width() + 6, mainpos.y() + 29)

        # Button connections
        self.export.push_right.clicked.connect(self.exp_push_cit_right)
        self.export.push_left.clicked.connect(self.exp_push_cit_left)
        self.export.copy_button.clicked.connect(self.exp_copy_to_clipboard)
        self.export.export_button.clicked.connect(self.exp_export_to_bibtex)

        # Actions on main window
        self.main.move_right.triggered.connect(self.exp_push_cit_right)

    def exp_push_cit_right(self):
        """Selected citation is copied to the export window and its index and name are displayed in the listwidget.
        :return: Nothing
        """

        # Selected items
        selected_cit = []

        # if no row is selected returns -1
        if self.main.citation_list.currentRow() >= 0:

            le = len(self.main.citation_list.selectedItems())

            # If number if selected rows is larger than 1
            if le > 6:
                for num in range(le // 6):
                    # Add all selected article indices to a list
                    selected_cit.append(self.main.citation_list.selectedItems()[num * 6].text())
            else:

                # Only one article is selected, add index to list
                selected_cit = [self.main.citation_list.selectedItems()[0].text()]

            # Get indices of articles in the export window
            index_list = self.export.list_of_indices()
            for el in selected_cit:

                # Check if selected item is already in the export window
                if el not in index_list:
                    name = self.all_articles[el].get_name()
                    if len(name) >= 12:
                        name = f'{name[:13]}...'
                    self.export.exp_cit_widget.addItem(f'{el}:\t[ {name} ]')

    def exp_push_cit_left(self):
        """Remove citation from the export list.
        :return: Nothing
        """
        self.export.exp_cit_widget.takeItem(self.export.exp_cit_widget.currentRow())

    def exp_copy_to_clipboard(self):
        """Get a list of all citations and copy their string representation to the clipboard
        :return: Nothing
        """
        copy = self.help_get_string_rep()

        # Copy the string to the clipboard
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(copy, mode=cb.Clipboard)

    def exp_export_to_bibtex(self):
        """Writes the BibTex string representations to a .bib file at a user defined directory.
        :return: Nothing
        """
        citations = self.help_get_string_rep()
        name = self.export.get_savefile_dialog()
        if name is not '':
            with open(name, 'w') as save:
                save.write(citations)

    # Add functions

    def show_add(self, name: str, path: str):
        """Shows the add GUI.
        :param name: Preassigned name of the new citation
        :return: Nothing
        """
        # Initialize add GUI
        self.add = add_GUI(SIZE_ADD, name)
        self.fp = path

        # Add connections
        self.add.accept.clicked.connect(self.add_new_citation)
        self.add.decline.clicked.connect(self.add.close)
        self.add.doiedit.editingFinished.connect(self.add_doi2bibtex)

    def add_new_citation(self):
        """Function that adds a new citation to the current citation list. Via entries int he add GUI the user can
        specify the BibTex information and the name. The citation list is immediately saved in the JSON save file.
        :return: Nothing
        """
        text = self.add.textedit.toPlainText()
        if text != '' and text[0] == "@" and text[-1] == "}":

            # Parameter for the new citation
            try:
                bibtex_dict = self.help_parse_latex(text)
            except:
                show_dialog('BibTex citations seems to be in a wrong format!', 'Error!')
                return

            ind = self.help_get_next_index()
            label = self.add.nameedit.text()
            tags = self.add.tagsedit.text().split(',')

            # Init of new citation
            cit = article(ind, label, self.fp, tags, asctime(), bibtex_dict, 0)

            if self.help_check_bibtex(bibtex_dict):
                if self.add.move.isChecked():
                    cit_title = cit.get_bibtex()["title"].lower().replace(" ", "_").replace(".", "").replace(",", "")
                    if len(cit_title) > 50:
                        cit_title = cit_title[:50]
                    title = f'{cit.get_index()}_{cit_title}.pdf'
                    cit.set_path(path.join(ARTICLE_SAVE, title))
                    if not path.exists(cit.get_path()):
                        rename(self.fp, cit.get_path())
                self.all_articles[str(cit.get_index())] = cit
                self.help_dump_to_json()
                self.currently_displayed.append(cit.get_index())
                if self.main is not None:
                    self.main_sort_and_display_articles()

            # update number of citations in the GUI
            self.afk.update_num_citations(self.help_get_next_index())
            self.add.close()

        else:
            show_dialog('BibTex citations seems to be in a wrong format!', 'Error!')

    def add_doi2bibtex(self):
        """If a DOI is entered in the DOI line edit, the DOI is searched for in the internet and the corresponding
        BibTex citation is inserted to the text field.
        :return: Nothing
        """

        # Thanks to https://scipython.com/blog/doi-to-bibtex/
        doi = self.add.doiedit.text()
        if doi != '':
            url = BASE_URL + doi
            req = urllib.request.Request(url)
            req.add_header('Accept', 'application/x-bibtex')

            try:
                with urllib.request.urlopen(req) as f:
                    self.add.textedit.setPlainText(f.read().decode())

            except:
                self.add.textedit.setPlainText("- [ The DOI could not be identified by the system."
                                               " Please paste your BibTex information here! ] -")

    # Settings functions

    def show_settings(self):
        """Displays the settings menu.
        :return: Nothing
        """
        self.settings_dialog = settings_dialog(SIZE_SET, self.settings)

        # Reposition export GUI next to main GUI
        mainpos = self.main.pos()
        # Relocate the export window
        mainsize = self.main.geometry()
        if sys.platform == "win32":
            self.settings_dialog.relocate(mainpos.x() + mainsize.width(), mainpos.y())
        else:
            self.settings_dialog.relocate(mainpos.x() + mainsize.width() + 6, mainpos.y() + 29)

        self.settings_dialog.cancel.clicked.connect(self.settings_dialog.close)
        self.settings_dialog.back.clicked.connect(lambda state, x=1: self.settings_dialog.pick_color(x))
        self.settings_dialog.font.clicked.connect(lambda state, x=2: self.settings_dialog.pick_color(x))
        self.settings_dialog.save.clicked.connect(self.sett_change_settings)

    def sett_change_settings(self):
        """Changes the settings of the windows to user input settings in the settings window.
        :return: Nothing
        """

        format = self.settings['NOTES_FORMAT']
        if self.settings_dialog.ret_settings() != {}:
            self.settings = self.settings_dialog.ret_settings()
        else:
            return
        with open(SETTINGS_JSON, "w") as file:
            json.dump(self.settings, file)

        new_format = self.settings['NOTES_FORMAT']
        if format != new_format:
            self.help_toggle_format()
        show_dialog("Files were successfully saved!", 'Success!')

    # Helper functions

    def help_toggle_format(self):
        """Changes the standard note format between Markdown and plain Text files.
        :return: Nothing
        """

        for art in self.all_articles.values():
            old_path = art.get_note_path()
            if old_path != '':
                if old_path[-1] == 't':
                    new_path = f'{old_path[:-4]}.md'
                else:
                    new_path = f'{old_path[:-3]}.txt'

                rename(old_path, new_path)
                art.set_note_path(new_path)

        self.help_dump_to_json()

    def help_dump_to_json(self):
        """All citations are saved in a JSON file.
        :return: Nothing
        """
        with open(SAVE_JSON, "w") as file:
            dic = {key: value.get_dict() for key, value in self.all_articles.items()}
            json.dump(dic, file)

    def help_check_bibtex(self, bibtex_dict):
        """Check if the text in the text field is already in the article list as bibtex citation. If this is the case
        the accept button is disabled. In case no text is provided in the text field the button is disabled as well.
        :return: Nothing
        """
        error = "The article seems to be in your system already!"

        # Loop through all articles in the list
        for ind, list_art in self.all_articles.items():

            if bibtex_dict == list_art.get_bibtex():
                show_dialog(error, 'Error!')
                return False
        return True

    def help_load_settings(self) -> dict:
        """Loads the settings from the setting JSON file, if it does not exist, it is created with standard settings.
        :return: Settings as dict
        """
        # Create save folder and json save file if not there
        if not path.exists(ARTICLE_SAVE):
            mkdir(ARTICLE_SAVE)
            with open(SETTINGS_JSON, 'w') as f:
                json.dump(STANDARD_SETTINGS, f)
        else:
            if not path.exists(SETTINGS_JSON):
                with open(SETTINGS_JSON, 'w') as f:
                    json.dump(STANDARD_SETTINGS, f)
            else:
                with open(SETTINGS_JSON, 'r') as f:
                    dic = json.load(f)
                    return dic
        return STANDARD_SETTINGS

    def help_load_articles(self) -> dict:
        """Checks if a .citation folder was created in the home directory before and if not it creates a new one.
        Further loads all citations from the JSON save file and creates a citation object out of every citation.
        :return: a dictionary with all citations as citation objects or an empty dictionary if no save file was found.
        """
        # Create save folder and json save file if not there
        if not path.exists(GENERAL):
            mkdir(GENERAL)

        # Init notes directory
        if not path.exists(NOTES_PATH):
            mkdir(NOTES_PATH)

        if not path.exists(ARTICLE_SAVE):
            mkdir(ARTICLE_SAVE)
            with open(SAVE_JSON, 'w') as f:
                json.dump(' ', f)
        else:
            if not path.exists(SAVE_JSON):
                with open(SAVE_JSON, 'w') as f:
                    json.dump(' ', f)
            else:
                with open(SAVE_JSON, 'r') as f:
                    dic = json.load(f)
                    if dic != ' ':
                        for ind, arts in dic.items():
                            dic[ind] = article(arts['id'], arts['name'],
                                               arts['path'], arts['tags'],
                                               arts['access'], arts['bibtex'],
                                               arts['relevance'], arts['note'])
                        return dic
        return {}

    def help_parse_latex(self, bibtexstr: str) -> dict:
        """The BibTex string that is put in the addition screen is parsed into a dictionary.
        :param bibtexstr: String that is put in the addition GUI
        :return: BibTex citation as dictionary
        """
        bp = BibTexParser(common_strings=True)
        bib_database = bp.parse(bibtexstr)
        return bib_database.entries[0]

    def help_gen_show_name(self, cit_index: int) -> list:
        """Generates a list of the displayed properties for a citation.
        :param cit_index: Index of the citation that is used.
        :return: list of properties that are displayed in the main GUI
        """
        key = str(cit_index)
        value = self.all_articles[key]
        name = value.get_name()
        tags = value.get_tags()

        # Add all tags to a string
        tags_part = ''
        for tag in tags:
            if tag != '':
                tags_part += f'[{tag}] '
        if tags_part == '':
            tags_part += 'no tags were assigned!'
        authors = value.get_bibtex()["author"]
        title = value.get_bibtex()["title"]
        return [key, name, tags_part, title, authors, value.get_bibtex()["year"]]

    def help_get_next_index(self) -> int:
        """Returns the next index of the main window citation list
        :return: Next index of the citation list
        """
        return len(self.all_articles)

    def help_get_string_rep(self) -> str:
        """Use a list of all indices that are in in the export list to generate a string representation of all
        citations.
        :return: BibTex string of all selected citations
        """
        # Receive a list of the indices of all selected articles
        index_list = self.export.list_of_indices()

        # Generate string that combines all selected citations
        fin = ''
        for index in index_list:
            fin += self.all_articles[index].bibtex_to_string() + '\n'

        return fin

    def help_move_window(self, window: QWidget):
        self.screensize = QDesktopWidget().screenGeometry()
        widget = window.geometry()
        x = self.screensize.width() - widget.width()
        window.move(x, 0)

    def help_open_file(self, filepath):
        # linux
        if sys.platform == 'linux':
            subprocess.call(["xdg-open", filepath])

        # macOS
        elif sys.platform == 'Darwin':
            subprocess.call(('open', filepath))

        # Windows
        else:
            startfile(filepath)

    def help_open_notes_folder(self):
        """Opens the folder that contains the notes
        :return: Nothing
        """
        self.help_open_file(NOTES_PATH)

    def help_open_article_folder(self):
        """Opens the folder that contains the articles
        :return: Nothing
        """
        self.help_open_file(ARTICLE_SAVE)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = control()
    sys.exit(app.exec_())

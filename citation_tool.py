# External libraries
import pprint
import subprocess
import sys
import json

from bibtexparser.bibdatabase import BibDataStringExpression
from bibtexparser.bparser import BibTexParser
from PyQt5.QtWidgets import QApplication
from time import asctime
from os import path, mkdir, rename

# Own stuff
from constants import BUTTON_COLOR_THEME1, CITATION_SAVE, SAVE_JSON, SIZE_MAIN, SIZE_ADD, SIZE_AFK, SIZE_EXP
from core import citation
from GUI import main_GUI, afk_GUI, add_GUI, export_GUI


class control:

    # Initialization of windows

    def __init__(self):
        # Init citations
        self.all_citations = self.open_citations()
        self.fp = None
        self.screensize = None

        # Init afk control gui
        self.afk = afk_GUI(SIZE_AFK, color=BUTTON_COLOR_THEME1, control=self)
        self.main = None
        self.add = None
        self.export = None

        # When the button is clicked the main window opens
        self.afk.button.clicked.connect(self.show_main)

    def open_citations(self) -> dict:
        # Create save folder and json save file if not there
        if not path.exists(CITATION_SAVE):
            mkdir(CITATION_SAVE)
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
                        for ind, cits in dic.items():
                            dic[ind] = citation(cits['id'], cits['name'],
                                                cits['path'], cits['tags'],
                                                cits['access'], cits['bibtex'])
                        return dic
        return {}

    def show_main(self):
        self.main = main_GUI(SIZE_MAIN, self)
        fin = []
        for ind, element in self.all_citations.items():
            fin.append(self.gen_show_name(ind))
        self.main.pop_list(fin)
        # Setting actions for main window
        self.main.citation_list.itemDoubleClicked.connect(self.open_pdf)
        self.main.export.triggered.connect(self.show_export)

    def show_export(self):
        self.export = export_GUI(SIZE_EXP, self)
        mainpos = self.main.pos()
        # Relocate the export window
        mainsize = self.main.geometry()
        self.export.relocate(mainpos.x() + mainsize.width() + 6, mainpos.y() + 29)

    def open_pdf(self):
        clicked_index = self.main.citation_list.selectedItems()[0].text()
        filepath = self.all_citations[clicked_index].get_path()

        # Opening the files only works on linux yet
        if sys.platform == 'linux':
            subprocess.call(["xdg-open", filepath])

    def gen_show_name(self, cit_index: int) -> list:
        key = cit_index
        value = self.all_citations[key]

        # Index
        index_part = f'\n {str(key)}' + (2 * ' ' if int(key) > 9 else ' ')
        # Name
        name = value.get_name()
        name_part = f'| {(name[:10] if len(name) > 9 else name + " "*10-len(name))} '
        # Tags
        tags = value.get_tags()
        tags_part = '| '
        for tag in tags:
            if tag != '':
                tags_part += f'[{tag}] '
        if tags_part == '| ':
            tags_part += 'no tags were assigned!'
        tags_part += ' '*(60-len(tags_part))
        # Year
        year_part = f'| {value.get_bibtex()["year"]} |\n'
        # Authors
        authors = value.get_bibtex()["author"]
        author_part = f'| {authors}' + " "*(40-len(authors)) if len(authors) < 40 else f'| {authors[:38]}.. '
        # Title
        title = value.get_bibtex()["title"]
        title_part = f'| {title}' + " "*(60-len(title)) if len(title) < 60 else f'| {title[:58]}.. '

        #return f'{index_part}{name_part}{tags_part}{title_part}{author_part}{year_part}'
        return [key, name, tags, title, authors, value.get_bibtex()["year"]]

    def show_add(self, name: str):
        self.add = add_GUI(SIZE_ADD, self, name)

        # Add connections
        self.add.accept.clicked.connect(self.new_citation)
        self.add.decline.clicked.connect(self.add.close)

    def get_next_index(self):
        return len(self.all_citations)

    # Add citations

    def parse_latex(self, bibtexstr: str):
        bp = BibTexParser(common_strings=True)
        bib_database = bp.parse(bibtexstr)
        return bib_database.entries[0]

    def new_citation(self):
        if self.add.textedit.toPlainText()[0] == "@":

            # Parameter for the new citation
            bibtex_dict = self.parse_latex(self.add.textedit.toPlainText())
            ind = self.get_next_index()
            label = self.add.nameedit.text()
            tags = self.add.tagsedit.text().split(',')

            # Init of new citation
            cit = citation(ind, label, self.fp, tags, asctime(), bibtex_dict)

            # Check if citation is in list already
            if self.check_for_duplicate(cit):
                if self.add.move.isChecked():
                    cit.set_path(CITATION_SAVE + '/' + self.fp.split('/')[-1])
                    rename(self.fp, cit.get_path())
                self.all_citations[cit.get_index()] = cit
                self.dump_to_json()

            # update number of citations in the GUI
            self.afk.update_num_citations()
            self.add.close()

    def set_filepath(self, filep: str):
        self.fp = filep

    def check_for_duplicate(self, cit: citation) -> bool:
        for ind, list_cit in self.all_citations.items():
            if cit.get_bibtex() == list_cit.get_bibtex():
                return False
        return True

    # Save citations to json file

    def dump_to_json(self):
        with open(SAVE_JSON, "w") as file:
            dic = {key: value.get_dict() for key, value in self.all_citations.items()}
            json.dump(dic, file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = control()
    sys.exit(app.exec_())

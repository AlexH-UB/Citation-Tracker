# External libraries
import pprint
import sys
import json
from bibtexparser.bparser import BibTexParser
from PyQt5.QtWidgets import QApplication
from time import asctime
from os import path, mkdir, rename

# Own stuff
from constants import BUTTON_COLOR_THEME1, CITATION_SAVE, SAVE_JSON
from core import citation
from GUI import main_GUI, afk_GUI, add_GUI


class control:

    # Initialization of windows

    def __init__(self):
        # Init citations
        self.all_citations = self.open_citations()
        self.fp = None

        # Init afk control gui
        self.afk = afk_GUI(size=(50, 50), color=BUTTON_COLOR_THEME1, control=self)
        self.main = None
        self.add = None

        # When the button is clicked the main window opens
        self.afk.button.clicked.connect(self.show_main)

    def open_citations(self) -> dict:
        # Create save folder and json save file if not there
        if not path.exists(CITATION_SAVE):
            mkdir(CITATION_SAVE)
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
        self.main = main_GUI((500, 500), self)

    def show_add(self, name: str):
        self.add = add_GUI((600, 500), self, name)
        self.add.accept.clicked.connect(self.new_citation)

    def get_next_index(self):
        return len(self.all_citations)

    # Add citations

    def parse_latex(self, bibtexstr: str):
        bp = BibTexParser(interpolate_strings=False)
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

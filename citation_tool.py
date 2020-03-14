# Own stuff
from constants import BUTTON_COLOR_THEME1
from core import citation
from GUI import main_GUI, afk_GUI, add_GUI

# External libraries

import sys
import json
from bibtexparser.bparser import BibTexParser
from PyQt5.QtWidgets import QApplication
from time import asctime


class control:

    # Initialization of windows

    def __init__(self):
        # Init citations list
        self.all_citations = {}
        self.fp = None

        # Init afk control gui
        self.afk = afk_GUI(size=(50, 50), color=BUTTON_COLOR_THEME1, control=self)
        self.main = None
        self.add = None

        # When the button is clicked the main window opens
        self.afk.button.clicked.connect(self.show_main)

    def show_main(self):
        self.main = main_GUI((500, 500), self)

    def show_add(self, name: str):
        self.add = add_GUI((400, 400), self, name)
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
                self.all_citations[cit.get_index()] = cit
                print(f"Added citation '{cit.get_name()}'.")
                self.dump_to_json('./Savespace/test1.json')

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

    def dump_to_json(self, filep: str):
        with open(filep, "w") as file:
            json.dump(self.all_citations, file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = control()
    sys.exit(app.exec_())

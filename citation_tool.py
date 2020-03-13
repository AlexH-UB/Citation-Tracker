from pprint import pprint
import sys, os

from bibtexparser.bparser import BibTexParser

from core import citation
from GUI import main_GUI, afk_GUI, add_GUI
from PyQt5.QtWidgets import QApplication
import json
from datetime import datetime


'''
TODO: Add general look (list widgets)
TODO: Add new citation mode 
TODO: Add search mode from button clicking afk gui
TODO: Make drag and drop possible (afk_GUI)
'''


# Example how to save stuff:
#
# all_citations.append(citation(len(all_citations),"First","dunno",[1,2,4,5,23,1],"now","citation with latex"))
# save_as_json("filename.json", all_citations[-1].to_dict())
#

class control:

    def __init__(self):
        # Init citations list
        self.all_citations = [None]

        # Init afk control gui
        self.afk = afk_GUI((50, 50), "slategray", self)
        self.main = None
        self.add = None

        # When the button is clicked the main window opens
        self.afk.button.clicked.connect(self.show_main)

    def show_main(self):
        self.main = main_GUI((500, 500), self)

    def show_add(self, name):
        self.add = add_GUI((400, 400), self, name)
        self.add.accept.clicked.connect(self.new_citation)

    def save_as_json(filename, text):
        with open(filename, "w") as file:
            json.dump(text, file)

    def get_next_index(self):
        return len(self.all_citations)

    def parse_latex(self, latex):
        bp = BibTexParser(interpolate_strings=False)
        bib_database = bp.parse(latex)
        return bib_database.entries[0]

    def new_citation(self):
        if self.add.textedit.toPlainText()[0] == "@":
            bibtex_dict = self.parse_latex(self.add.textedit.toPlainText())
            ind = self.get_next_index()
            label = self.add.nameedit.text()
            tags = self.add.tagsedit.text().split(',')
            self.all_citations.append(citation(ind, label, self.fp, tags, datetime(), bibtex_dict))
            pprint(bibtex_dict)
            pprint(self.all_citations)

    def set_filepath(self, filepath):
        self.fp = filepath


"""
Example citation:

@article{gayvert2016computational,
title={A computational drug repositioning approach for targeting oncogenic transcription factors},
author={Gayvert, Kaitlyn M and Dardenne, Etienne and Cheung, Cynthia and Boland, Mary Regina and Lorberbaum, Tal and Wanjala, Jackline and Chen, Yu and Rubin, Mark A and Tatonetti, Nicholas P and Rickman, David S and others},
journal={Cell reports},
volume={15},
number={11},
pages={2348--2356},
year={2016},
publisher={Elsevier}
}

"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = control()
    sys.exit(app.exec_())

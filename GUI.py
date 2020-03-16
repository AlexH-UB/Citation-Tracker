from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTextEdit, QCheckBox, \
    QDesktopWidget, QMainWindow, QListWidget, QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from constants import EXAMPLE_CITATION, TITLE_ADD, TITLE_MAIN, LABEL_NAME, LABEL_TAGS, LABEL_BIBTEX, FONT_SIZE, \
    TITLE_EXPORT


class afk_GUI(QWidget):

    def __init__(self, size, color, control):
        super().__init__()

        # Setting up the main GUI
        self.setFixedSize(size[0], size[1])
        self.control = control
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.move_window()

        # Setting up the main button
        num_cit = self.control.get_next_index()
        self.button = dnd_button(str(num_cit), self)
        self.button.resize(size[0], size[1])
        self.button.setStyleSheet(f'background-color: {color[0]}; color: {color[1]};')

        self.show()

    def move_window(self):
        self.control.screensize = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = self.control.screensize.width() - widget.width()
        self.move(x, 0)

    def update_num_citations(self):
        self.button.setText(str(self.control.get_next_index()))


class main_GUI(QMainWindow):

    def __init__(self, wh, control):
        super().__init__()

        # Setting up the side GUI
        self.setFixedSize(wh[0], wh[1])
        self.setWindowTitle(TITLE_MAIN)
        self.control = control

        # Init menu bar
        menu = self.menuBar().addMenu('File')
        self.export = menu.addAction("Export")

        # Init of main window stuff
        maingrid = QGridLayout()
        maingrid.setSpacing(50)

        toplayout = QGridLayout()
        maingrid.addLayout(toplayout, 0, 0)
        toplayout.addWidget(QLabel("test"), 0, 0)
        toplayout.addWidget(QLabel("test"), 0, 1)
        toplayout.addWidget(QLabel("Searchbar"), 0, 2)

        toplayout.addWidget(QLabel("test"), 1, 0)
        toplayout.addWidget(QLabel("test"), 1, 1)
        toplayout.addWidget(QLabel("Filter stuff"), 1, 2)

        self.citation_list = QListWidget()
        font = QFont()
        font.setPointSize(FONT_SIZE)
        self.citation_list.setFont(font)

        maingrid.addWidget(self.citation_list, 1, 0)
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(maingrid)
        self.show()

    def pop_list(self, names: list):
        self.citation_list.addItems(names)


class add_GUI(QWidget):

    def __init__(self, wh, control, name):
        super().__init__()

        # Setting up the side GUI
        self.setFixedSize(wh[0], wh[1])
        grid = QGridLayout()
        grid.setSpacing(10)

        # Create label and line edit to enter a short name for the citation
        grid.addWidget(QLabel(LABEL_NAME), 0, 0)
        self.nameedit = QLineEdit(name)
        grid.addWidget(self.nameedit, 0, 1)

        # Create label and line edit to enter a list of tags to identify the citation
        grid.addWidget(QLabel(LABEL_TAGS), 1, 0)
        self.tagsedit = QLineEdit()
        grid.addWidget(self.tagsedit, 1, 1)

        # Create text field for citation information in bibTex format
        self.latexlab = QLabel(LABEL_BIBTEX)
        self.latexlab.setAlignment(Qt.AlignTop)
        grid.addWidget(self.latexlab, 2, 0)
        self.textedit = QTextEdit(EXAMPLE_CITATION)
        grid.addWidget(self.textedit, 2, 1)

        # Add Accept and cancel button
        self.accept = QPushButton('Add to Library')
        self.decline = QPushButton('Cancel')
        self.move = QCheckBox('Move file')
        self.move.setChecked(True)

        grid.addWidget(self.decline, 3, 0)
        grid.addWidget(self.accept, 3, 1)
        grid.addWidget(self.move, 3, 2)

        # Final init steps
        self.setLayout(grid)
        self.setWindowTitle(TITLE_ADD)
        self.control = control

        self.show()


class export_GUI(QWidget):

    def __init__(self, wh, control):
        super().__init__()

        # Setting up the side GUI
        self.setFixedSize(wh[0], wh[1])
        self.setWindowTitle(TITLE_EXPORT)
        self.control = control

        grid = QGridLayout()
        grid.setSpacing(30)
        self.label2 = QLabel("Whatup this is label 2waegwegweg4wge4wg4wg4w4gwgwg4wg4")
        self.exp_cit_widget = QListWidget()
        self.copy_button = QPushButton()
        self.export_button = QPushButton()
        self.push_right = QPushButton("->")
        self.push_left = QPushButton("<-")

        # Setting the widgets up on the GUI
        #grid.addWidget(self.label2, 0, 0, 1, 2)
        grid.addWidget(self.exp_cit_widget, 0, 1, 4, 2)
        grid.addWidget(self.push_right, 1, 0)
        grid.addWidget(self.push_left, 2, 0)
        grid.addWidget(self.copy_button, 4, 1)
        grid.addWidget(self.export_button, 4, 2)

        grid.setColumnStretch(0, 0.5)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 2)

        self.setLayout(grid)
        self.show()

    def relocate(self, x, y):
        self.move(x, y)


class dnd_button(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.parent = parent

    def dragEnterEvent(self, e):
        if e.mimeData().text()[-4:] == '.pdf':
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.parent.control.show_add(e.mimeData().text().split('/')[-1][:-4])
        self.parent.control.set_filepath(e.mimeData().text()[7:])

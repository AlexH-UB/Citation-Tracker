from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTextEdit, QCheckBox, \
    QDesktopWidget, QMainWindow, QListWidget, QTableWidget, QTableWidgetItem, QTableView, QComboBox, \
    QFileDialog, QAction

from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QKeySequence

from constants import EXAMPLE_CITATION, TITLE_ADD, TITLE_MAIN, LABEL_NAME, LABEL_TAGS, LABEL_BIBTEX, FONT_SIZE, \
    TITLE_EXPORT, LABEL_TABLE, MOVE_LEFT, MOVE_RIGHT, QUICK_COPY, OPEN_EXPORT


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
        """The afk window is moved to the top right corner and can be used from this position.
        :return: Nothing
        """
        self.control.screensize = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = self.control.screensize.width() - widget.width()
        self.move(x, 0)

    def update_num_citations(self):
        """The number of citations in the citation list is displayed in the afk GUI.
        :return: Nothing
        """
        self.button.setText(str(self.control.get_next_index()))


class main_GUI(QMainWindow):

    def __init__(self, wh, control):
        super().__init__()

        # Setting up the side GUI
        self.setFixedSize(wh[0], wh[1])
        self.setWindowTitle(TITLE_MAIN)
        self.control = control

        # Init of main window stuff
        maingrid = QGridLayout()
        maingrid.setSpacing(50)

        toplayout = QGridLayout()
        toplayout.setAlignment(Qt.AlignRight)
        maingrid.addLayout(toplayout, 0, 0)

        self.searchbar = QLineEdit("Search..")
        self.combo = QComboBox()
        self.combo.addItem('Index ↓')
        self.combo.addItem('Index ↑')
        self.combo.addItem('Relevance ↓')
        self.combo.addItem('Relevance ↑')

        toplayout.setColumnStretch(0, 1)
        toplayout.setColumnStretch(1, 1)
        toplayout.setColumnStretch(2, 1)
        toplayout.setColumnStretch(3, 1)
        toplayout.setColumnStretch(4, 1)
        toplayout.setColumnStretch(5, 1)

        toplayout.addWidget(QLabel("test"), 0, 0)
        toplayout.addWidget(QLabel("test"), 0, 1)
        toplayout.addWidget(QLabel("test"), 0, 2)
        toplayout.addWidget(QLabel("test"), 0, 3)
        toplayout.addWidget(QLabel("test"), 0, 4)
        toplayout.addWidget(self.searchbar, 0, 5)

        toplayout.addWidget(QLabel("test"), 1, 0)
        toplayout.addWidget(QLabel("test"), 1, 1)
        toplayout.addWidget(QLabel("test"), 1, 2)
        toplayout.addWidget(QLabel("test"), 1, 3)
        toplayout.addWidget(QLabel("test"), 1, 4)
        toplayout.addWidget(self.combo, 1, 5)

        self.citation_list = QTableWidget(6, 6)
        self.citation_list.setSelectionBehavior(QTableView.SelectRows)
        font = QFont()
        font.setPointSize(FONT_SIZE)
        self.citation_list.setFont(font)
        self.citation_list.setHorizontalHeaderLabels(LABEL_TABLE)

        # Column widths
        self.citation_list.setColumnWidth(0, 60)
        self.citation_list.setColumnWidth(1, 150)
        self.citation_list.setColumnWidth(2, 400)
        self.citation_list.setColumnWidth(3, 350)
        self.citation_list.setColumnWidth(4, 400)
        self.citation_list.setColumnWidth(5, 70)
        self.citation_list.verticalHeader().setVisible(False)
        self.citation_list.setEditTriggers(QTableWidget.NoEditTriggers)

        # Actions

        self.move_right = QAction('&Move to export', self)
        self.move_right.setShortcut(QKeySequence(MOVE_RIGHT))

        self.show_exp = QAction('&Open export', self)
        self.show_exp.setShortcut(QKeySequence(OPEN_EXPORT))

        self.quick_copy = QAction('&Quick copy BibTex', self)
        self.quick_copy.setShortcut(QKeySequence(QUICK_COPY))

        # Init menu bar
        menu = self.menuBar().addMenu('Articles')
        menu.addAction(self.quick_copy)
        menu.addSeparator()
        menu.addAction(self.show_exp)
        menu.addAction(self.move_right)

        maingrid.addWidget(self.citation_list, 1, 0)
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(maingrid)
        self.show()

    def pop_list(self, names: list):
        """Populates the tablewidget on the main_GUI with a list of strings.
        :param names: list of strings
        :return: Nothing
        """
        # list of lists
        self.citation_list.setRowCount(0)
        self.citation_list.setRowCount(len(names))
        for ind, value in enumerate(names):
            for ind2, value2 in enumerate(value):
                item = QTableWidgetItem(str(value2))
                if ind2 == 0 or ind2 == 5:
                    item.setTextAlignment(Qt.AlignCenter)
                self.citation_list.setItem(ind, ind2, item)


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
        self.exp_cit_widget = QListWidget()

        # Initialize buttons
        self.copy_button = QPushButton('Copy')
        self.export_button = QPushButton('Export to BibTex')
        self.push_right = QPushButton("->")
        self.push_left = QPushButton("<-")

        # Setting the widgets up on the GUI
        grid.addWidget(self.exp_cit_widget, 0, 1, 4, 2)
        grid.addWidget(self.push_right, 1, 0)
        grid.addWidget(self.push_left, 2, 0)
        grid.addWidget(self.copy_button, 4, 1)
        grid.addWidget(self.export_button, 4, 2)

        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 2)

        self.setLayout(grid)
        self.show()

    def relocate(self, x, y):
        """Relocates the export GUI to the coordinate x and y.
        :param x: horizontal coordinate
        :param y: vertical coordinate
        :return: Nothing
        """
        self.move(x, y)

    def list_of_indices(self) -> list:
        """Generates a list of all indices of the articles that were selected to be exported.
        :return: List of all indices of the articles that were selected to be exported.
        """
        return [self.exp_cit_widget.item(i).text()[0]
                for i in range(self.exp_cit_widget.count())]

    def get_savefile_dialog(self) -> str:
        """Opens a file dialog window to determine the directory the BibTex file is saved in.
        :return: Path of the BibTex file as string
        """
        return QFileDialog.getSaveFileName(self, "Save articles in BibTex")[0]


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

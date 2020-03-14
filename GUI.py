from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTextEdit, QGroupBox, QDesktopWidget
from PyQt5 import QtCore
from constants import EXAMPLE_CITATION, TITLE_ADD, TITLE_MAIN, LABEL_NAME, LABEL_TAGS, LABEL_BIBTEX


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
        screen = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = screen.width() - widget.width()
        self.move(x, 0)

    def update_num_citations(self):
        self.button.setText(str(self.control.get_next_index()))


class main_GUI(QWidget):

    def __init__(self, wh, control):
        super().__init__()

        # Setting up the side GUI
        self.setFixedSize(wh[0], wh[1])
        self.setWindowTitle(TITLE_MAIN)
        self.control = control

        # Hier kommt alles vom main window hin

        self.show()


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
        self.decline.clicked.connect(self.close)
        grid.addWidget(self.decline, 3, 0)
        grid.addWidget(self.accept, 3, 1)


        # Final init steps
        self.setLayout(grid)
        self.setWindowTitle(TITLE_ADD)
        self.control = control

        self.show()


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

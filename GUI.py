from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTextEdit, QGroupBox, QDesktopWidget
from PyQt5 import QtCore
from time import asctime


class afk_GUI(QWidget):

    def __init__(self, wh, color, control):
        super().__init__()

        # Setting up the main GUI
        self.setFixedSize(wh[0], wh[1])
        self.control = control
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.move_window()

        # Setting up the main button
        self.button = custButton("", self)
        self.button.resize(wh[0], wh[1])
        self.button.setStyleSheet("background-color: {}".format(color))

        self.show()

    def move_window(self):
        screen = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = screen.width() - widget.width()
        self.move(x, 0)


class main_GUI(QWidget):

    def __init__(self, wh, control):
        super().__init__()

        # Setting up the side GUI
        self.setFixedSize(wh[0], wh[1])
        self.setWindowTitle('main_GUI')
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

        # Create two labels for index and the actual number
        grid.addWidget(QLabel('Label:'), 0, 0)
        self.nameedit = QLineEdit(name)
        grid.addWidget(self.nameedit, 0, 1)

        grid.addWidget(QLabel('Tags:'), 1, 0)
        self.tagsedit = QLineEdit("")
        grid.addWidget(self.tagsedit, 1, 1)

        # Create bibText field
        self.latexlab = QLabel('Latex:')
        self.latexlab.setAlignment(Qt.AlignTop)
        grid.addWidget(self.latexlab, 2, 0)
        self.textedit = QTextEdit('')
        grid.addWidget(self.textedit, 2, 1)

        # Add two buttons
        self.accept = QPushButton('Add to Library')
        self.decline = QPushButton('Cancel')
        self.decline.clicked.connect(self.close)
        grid.addWidget(self.decline, 3, 0)
        grid.addWidget(self.accept, 3, 1)


        # Final steps
        self.setLayout(grid)
        self.setWindowTitle('GUI for adding papers')
        self.control = control

        self.show()


class custButton(QPushButton):

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
        print(e.mimeData().text()[7:])
        print(e.mimeData().text().split('/')[-1][:-4])
        self.parent.control.show_add(e.mimeData().text().split('/')[-1][:-4])
        self.parent.control.set_filepath(e.mimeData().text()[7:])

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTextEdit, QCheckBox, \
    QMainWindow, QListWidget, QTableWidget, QTableWidgetItem, QTableView, QComboBox, QFileDialog, QAction,\
    QColorDialog, QMessageBox

from os import path
import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QKeySequence, QIcon

from constants import TITLE_ADD, TITLE_MAIN, LABEL_NAME, LABEL_TAGS, LABEL_BIBTEX, FONT_SIZE, \
    TITLE_EXPORT, LABEL_TABLE, LOGO_PATH, SIZE_AND_BUTTON, EXPLAIN_TEXT, TITLE_SETTINGS, TITLE_CHANGE


class afk_GUI(QWidget):

    # GUI that is always displayed in the top right corner

    def __init__(self, size, color, num_cit):
        super().__init__()

        # Setting up the main GUI
        self.setFixedSize(size[0], size[1])
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowIcon(QIcon(LOGO_PATH))

        # Setting up the main button
        self.button = dnd_button(str(num_cit), self)
        self.button.resize(size[0], size[1])
        self.button.setStyleSheet(f'background-color: {color[0]}; color: {color[1]};')

        self.show()

    def update_num_citations(self, number: int):
        """The number of citations in the citation list is displayed in the afk GUI.
        :return: Nothing
        """
        self.button.setText(str(number))


class add_GUI(QWidget):

    # Displayed when an article should be added to the system

    def __init__(self, wh, name):
        super().__init__()

        # Setting up the side GUI
        self.setFixedSize(wh[0], wh[1])
        grid = QGridLayout()
        grid.setSpacing(10)
        self.setWindowIcon(QIcon(LOGO_PATH))

        # Create label and line edit to enter a short name for the citation
        grid.addWidget(QLabel(LABEL_NAME), 0, 0)
        self.nameedit = QLineEdit(name)
        grid.addWidget(self.nameedit, 0, 1)

        # Create label and line edit to enter a list of tags to identify the citation
        grid.addWidget(QLabel(LABEL_TAGS), 1, 0)
        self.tagsedit = QLineEdit()
        grid.addWidget(self.tagsedit, 1, 1)

        # Create label and line edit to enter the DOI of an article to generate the BibTex from it
        grid.addWidget(QLabel('DOI'), 2, 0)
        self.doiedit = QLineEdit()
        grid.addWidget(self.doiedit, 2, 1)

        # Create text field for citation information in bibTex format
        self.latexlab = QLabel(LABEL_BIBTEX)
        self.latexlab.setAlignment(Qt.AlignTop)
        grid.addWidget(self.latexlab, 3, 0)
        self.textedit = QTextEdit('')
        grid.addWidget(self.textedit, 3, 1, 2, 1)

        # Add Accept and cancel button
        self.accept = QPushButton('Add to Library')
        self.decline = QPushButton('Cancel')
        self.move = QCheckBox('Move file')
        self.move.setChecked(True)

        grid.addWidget(self.decline, 5, 0)
        grid.addWidget(self.accept, 5, 1)
        grid.addWidget(self.move, 4, 0)

        # Final init steps
        self.setLayout(grid)
        self.setWindowTitle(TITLE_ADD)

        self.show()


class main_GUI(QMainWindow):

    # Main Interaction Point

    def __init__(self, wh, hide_explain, shortcuts):
        super().__init__()

        # Setting up the side GUI
        self.setFixedSize(wh[0], wh[1])
        self.setWindowTitle(TITLE_MAIN)
        self.setWindowIcon(QIcon(LOGO_PATH))

        # Init of main window stuff
        maingrid = QGridLayout()
        maingrid.setSpacing(10)

        toplayout = QGridLayout()
        toplayout.setAlignment(Qt.AlignRight)
        maingrid.addLayout(toplayout, 0, 0)

        self.searchbar = QLineEdit("Search..")
        self.combo = QComboBox()
        self.combo.addItem('Index ↓')
        self.combo.addItem('Index ↑')
        self.combo.addItem('Relevance ↓')
        self.combo.addItem('Relevance ↑')

        self.add_button = QPushButton('and')
        self.add_button.setMaximumSize(QSize(SIZE_AND_BUTTON[0], SIZE_AND_BUTTON[1]))
        self.explain_label = QLabel(EXPLAIN_TEXT)
        self.explain_label.setWordWrap(True)
        self.explain_label.setOpenExternalLinks(True)
        self.explain_label.setVisible(not hide_explain)

        toplayout.addWidget(self.explain_label, 0, 0)
        toplayout.addWidget(self.add_button, 0, 1)
        toplayout.addWidget(self.searchbar, 0, 2)
        toplayout.addWidget(self.combo, 1, 2)

        toplayout.setAlignment(self.add_button, Qt.AlignTop)
        toplayout.setAlignment(self.combo, Qt.AlignBottom)
        toplayout.setAlignment(self.searchbar, Qt.AlignTop)
        toplayout.setAlignment(self.explain_label, Qt.AlignTop)

        self.citation_list = QTableWidget(6, 6)
        self.citation_list.setSelectionBehavior(QTableView.SelectRows)
        font = QFont()
        font.setPointSize(FONT_SIZE)
        self.citation_list.setFont(font)
        self.citation_list.setHorizontalHeaderLabels(LABEL_TABLE)

        # Column widths
        toplayout.setColumnMinimumWidth(0, 1000)
        toplayout.setColumnMinimumWidth(1, 60)
        toplayout.setColumnMinimumWidth(2, 100)
        toplayout.setSpacing(50)
        toplayout.setRowMinimumHeight(1, 50)
        toplayout.setRowMinimumHeight(0, 50)

        self.citation_list.setColumnWidth(0, 60)
        self.citation_list.setColumnWidth(1, 150)
        self.citation_list.setColumnWidth(2, 400)
        self.citation_list.setColumnWidth(3, 350)
        self.citation_list.setColumnWidth(4, 380)
        self.citation_list.setColumnWidth(5, 70)
        self.citation_list.verticalHeader().setVisible(False)
        self.citation_list.setEditTriggers(QTableWidget.NoEditTriggers)

        # Actions

        self.move_right = QAction('&Move to export', self)
        self.move_right.setShortcut(QKeySequence(shortcuts['Move citation to export:']))

        self.show_exp = QAction('&Open export', self)
        self.show_exp.setShortcut(QKeySequence(shortcuts['Open the export window:']))

        self.quick_copy = QAction('&Quick copy BibTex', self)
        self.quick_copy.setShortcut(QKeySequence(shortcuts['Quick copy a citation:']))

        self.delete_article = QAction('&Delete Article', self)
        self.delete_article.setShortcut(QKeySequence.Delete)

        self.show_settings = QAction('&Settings', self)
        self.show_settings.setShortcut(QKeySequence(shortcuts['Show the settings menu:']))

        self.change_article = QAction('&Change entry')
        self.change_article.setShortcut(QKeySequence(shortcuts['Change entry:']))

        self.close_all_windows = QAction('&Close all windows')
        self.close_all_windows.setShortcut(QKeySequence(shortcuts['Close all windows:']))

        # Init menu bar
        article_menu = self.menuBar().addMenu('Articles')
        article_menu.addAction(self.quick_copy)
        article_menu.addAction(self.change_article)
        article_menu.addAction(self.delete_article)
        article_menu.addSeparator()
        article_menu.addAction(self.show_exp)
        article_menu.addAction(self.move_right)
        article_menu.addSeparator()
        article_menu.addAction(self.show_settings)
        article_menu.addAction(self.close_all_windows)

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


class change_article_GUI(QWidget):

    # Displayed when article information should be changed

    def __init__(self, wh, dic, bibtex):
        super().__init__()

        # Setting up the side GUI
        self.setFixedSize(wh[0], wh[1])
        grid = QGridLayout()
        grid.setSpacing(10)
        self.setWindowIcon(QIcon(LOGO_PATH))

        # Create label and line edit to enter a short name for the citation
        grid.addWidget(QLabel(LABEL_NAME), 0, 0)
        self.nameedit = QLineEdit(dic['name'])
        grid.addWidget(self.nameedit, 0, 1)

        # Create label and line edit to enter a list of tags to identify the citation
        grid.addWidget(QLabel(LABEL_TAGS), 1, 0)
        self.tagsedit = QLineEdit(','.join(dic['tags']))
        grid.addWidget(self.tagsedit, 1, 1)

        # Create text field for citation information in bibTex format
        self.latexlab = QLabel(LABEL_BIBTEX)
        self.latexlab.setAlignment(Qt.AlignTop)
        grid.addWidget(self.latexlab, 3, 0)
        self.textedit = QTextEdit(bibtex)
        grid.addWidget(self.textedit, 3, 1, 2, 1)

        # Add Accept and cancel button
        self.accept = QPushButton('Change entry')
        self.decline = QPushButton('Cancel')

        grid.addWidget(self.decline, 5, 0)
        grid.addWidget(self.accept, 5, 1)

        # Final init steps
        self.setLayout(grid)
        self.setWindowTitle(TITLE_CHANGE)

        self.show()


class export_GUI(QWidget):

    # Displayed when citations should be exported

    def __init__(self, wh):
        super().__init__()

        # Setting up the side GUI
        self.setFixedSize(wh[0], wh[1])
        self.setWindowTitle(TITLE_EXPORT)
        self.setWindowIcon(QIcon(LOGO_PATH))

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


class settings_dialog(QWidget):

    # Displayed when the settings should be changed

    def __init__(self, wh, settings):
        super().__init__()
        self.resize(QSize(wh[0], wh[1]))
        self.setWindowIcon(QIcon(LOGO_PATH))
        self.setWindowTitle(TITLE_SETTINGS)

        size_main = settings['SIZE_MAIN']
        size_afk = settings['SIZE_AFK']
        button_color = settings['BUTTON_COLOR']
        hide_explain = settings['HIDE_EXPLAIN']

        # Initialize grid layout

        grid = QGridLayout()
        grid.setSpacing(10)

        # Initialize widgets
        setting = QLabel('Settings')
        font1 = QFont()
        font1.setBold(True)
        setting.setFont(font1)

        grid.addWidget(setting, 0, 0)
        grid.addWidget(QLabel('Size main (px):'), 1, 0)
        self.main_width = QLineEdit(str(size_main[0]))
        self.main_height = QLineEdit(str(size_main[1]))
        grid.addWidget(self.main_width, 1, 1)
        grid.addWidget(self.main_height, 1, 2)

        grid.addWidget(QLabel('Size afk  (px):'), 2, 0)
        self.afk_width = QLineEdit(str(size_afk[0]))
        self.afk_height = QLineEdit(str(size_afk[1]))
        grid.addWidget(self.afk_width, 2, 1)
        grid.addWidget(self.afk_height, 2, 2)

        grid.addWidget(QLabel('Background'), 3, 1, alignment=Qt.AlignBottom)
        grid.addWidget(QLabel('Font'), 3, 2, alignment=Qt.AlignBottom)

        grid.addWidget(QLabel('Button color theme:'), 4, 0)
        self.back = QPushButton(button_color[0])
        self.back.setStyleSheet(f'background-color: {button_color[0]}; color: black')
        self.font = QPushButton(button_color[1])
        self.font.setStyleSheet(f'background-color: {button_color[1]}; color: black')
        grid.addWidget(self.back, 4, 1)
        grid.addWidget(self.font, 4, 2)

        grid.addWidget(QLabel('Hide explain text:'), 5, 0)
        self.checkbox = QCheckBox('')
        self.checkbox.setChecked(hide_explain)
        grid.addWidget(self.checkbox, 5, 1)

        short = QLabel('Shortcuts:')
        short.setFont(font1)
        short.setAlignment(Qt.AlignBottom)
        grid.addWidget(short, 6, 0)

        self.table = QTableWidget(len(settings['SHORTCUTS'].keys()), 2)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setColumnWidth(0, 275)
        self.table.setColumnWidth(1, 100)

        c = 0
        for text, value in settings['SHORTCUTS'].items():
            item = QTableWidgetItem(text)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(c, 0, item)
            item.setTextAlignment(Qt.AlignVCenter)

            item = QTableWidgetItem(value)
            self.table.setItem(c, 1, item)
            item.setTextAlignment(Qt.AlignVCenter)
            c += 1

        grid.addWidget(self.table, 7, 0, 3, 3)

        self.cancel = QPushButton('Cancel')
        self.cancel.setFixedWidth(125)

        self.save = QPushButton('Save')
        self.save.setFixedWidth(125)
        grid.addWidget(self.cancel, 10, 0)
        grid.addWidget(self.save, 10, 2)

        self.setLayout(grid)
        self.show()

    def pick_color(self, b):
        """Opens a color picker to determine a color.
        :param b: 1 if background, 2 of font color.
        :return: Nothing
        """
        co = QColorDialog.getColor().name()
        if co is not None:
            if b == 1:
                self.back.setText(co)
                self.back.setStyleSheet(f'background-color: {co}')

            elif b == 2:
                self.font.setText(co)
                self.font.setStyleSheet(f'background-color: {co}')

    def ret_settings(self) -> dict:
        """Takes all settings from the settings dialog, checks if they are correct and returns them as dict.
        :return: User provided settings as dict or empty dict if settings have errors in them.
        """
        dic = {}
        try:
            main_w = int(self.main_width.text())
            main_h = int(self.main_height.text())
            if main_w > 0 and main_h > 0:
                dic['SIZE_MAIN'] = (main_w, main_h)
        except:
            show_dialog('Main Size is required to be over 0 and with only numberical characters!', 'Error!')
            return {}

        try:
            afk_w = int(self.afk_width.text())
            afk_h = int(self.afk_height.text())
            if afk_w > 0 and afk_h > 0:
                dic['SIZE_AFK'] = (afk_w, afk_h)
        except:
            show_dialog('Afk Size is required to be over 0 and with only numberical characters!', 'Error!')
            return {}

        dic['BUTTON_COLOR'] = (self.back.text(), self.font.text())
        dic['HIDE_EXPLAIN'] = self.checkbox.isChecked()

        s_dic = {}
        save = None
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                if column == 0:
                    save = self.table.item(row, column).text()
                elif column == 1:
                    s_dic[save] = self.table.item(row, column).text()
        dic['SHORTCUTS'] = s_dic

        return dic

    def relocate(self, x, y):
        """Relocates the export GUI to the coordinate x and y.
        :param x: horizontal coordinate
        :param y: vertical coordinate
        :return: Nothing
        """
        self.move(x, y)


class dnd_button(QPushButton):
    # QPushbutton with drag and drop functions overwritten
    dropped = QtCore.pyqtSignal(str, str)

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.parent = parent

    def dragEnterEvent(self, e):
        urls = e.mimeData().urls()
        if len(urls) == 1 and urls[0].toString()[-4:] == '.pdf':
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        url = e.mimeData().urls()[0].toString()
        if sys.platform == 'win32':
            self.dropped.emit(url.split('/')[-1][:-4], url[8:].replace('/', '\\'))
        else:
            self.dropped.emit(url.split(path.sep)[-1][:-4], url[7:])


def show_dialog(text, title):
    """Shows a dialog window if there are messages that need to be reported to the user.
    :param text: Text that is on the dialog
    :param title: Title of the dialog
    :return: Nothing
    """
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(text)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.buttonClicked.connect(msgBox.close)
    msgBox.exec()

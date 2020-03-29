from os.path import expanduser, join, sep
from random import choice

# Constants

EXAMPLE_CITATION1 = '@article{Fuss2006,' \
                    '  doi = {10.1038/nature05412},' \
                    '  url = {https://doi.org/10.1038/nature05412},' \
                    '  year = {2006},' \
                    '  month = dec,' \
                    '  publisher = {Springer Science and Business Media {LLC}},' \
                    '  volume = {444},' \
                    '  number = {7121},' \
                    '  pages = {945--948},' \
                    '  author = {Bernhard Fuss and Thomas Becker and Ingo Zinke and Michael Hoch},' \
                    '  title = {The cytohesin Steppke is essential for insulin signalling in Drosophila},' \
                    '  journal = {Nature}' \
                    '}'

EXAMPLE_CITATION2 = '@article{Becker2010,' \
                    '  doi = {10.1038/nature08698},' \
                    '  url = {https://doi.org/10.1038/nature08698},' \
                    '  year = {2010},' \
                    '  month = jan,' \
                    '  publisher = {Springer Science and Business Media {LLC}},' \
                    '  volume = {463},' \
                    '  number = {7279},' \
                    '  pages = {369--373},' \
                    '  author = {Thomas Becker and Gerrit Loch and Marc Beyer and Ingo Zinke and Anna C. Aschenbrenner' \
                    ' and Pilar Carrera and Therese Inhester and Joachim L. Schultze and Michael Hoch}, ' \
                    '  title = {{FOXO}-dependent regulation of innate immune homeostasis},' \
                    '  journal = {Nature}}'

EXAMPLE_CITATION3 = '@article{Mass2014,' \
                    '  doi = {10.1016/j.devcel.2014.02.012},' \
                    '  url = {https://doi.org/10.1016/j.devcel.2014.02.012},' \
                    '  year = {2014},' \
                    '  month = mar,' \
                    '  publisher = {Elsevier {BV}},' \
                    '  volume = {28},' \
                    '  number = {6},' \
                    '  pages = {711--726},' \
                    '  author = {Elvira Mass and Dagmar Wachten and Anna~C. Aschenbrenner and Andr{\'{e}} Voelzmann and Michael Hoch},' \
                    '  title = {Murine Creld1 Controls Cardiac Development through Activation of Calcineurin/{NFATc}1 Signaling},' \
                    '  journal = {Developmental Cell}' \
                    '}'

EXAMPLE_CITATION = choice([EXAMPLE_CITATION1, EXAMPLE_CITATION2, EXAMPLE_CITATION3])


VERSION = "beta 1.0"
NAME = f"Alex's Citation Manager Version {VERSION}"
FONT_SIZE = 11
EXPLAIN_TEXT = f'Welcome to {NAME}. The purpose of this app is to help you keep track of your articles. When ' \
               f'inserting an article, it should be tagged with 1-10 short tags that describe it as well as possible. ' \
               f'This way it is much easier to organize and find your articles later in time. Articles can be moved ' \
               f'to a specific article folder in your home directory and opened by double clicking the articles in ' \
               f' this window. For a more detailed description and explanation of all functions check out the ' \
               f'<a href="https://github.com/AlexH-UB/Citation-Tracker">How to use page on my Github</a>. Thanks ' \
               f'for using.'

# Window titles

TITLE_MAIN = f'Main Interaction Point - {NAME}'
TITLE_ADD = f'Add a Citation - {NAME}'
TITLE_EXPORT = 'Export your citations'
TITLE_SETTINGS = f'Settings'

# Window Sizes

SIZE_ADD = (500, 500)
SIZE_EXP = (400, 650)
SIZE_SET = (400, 650)

SIZE_AND_BUTTON = (60, 30)

# GUI labels names

LABEL_NAME = 'Label:'
LABEL_TAGS = 'Tags:'
LABEL_BIBTEX = 'BibTex:'
LABEL_TABLE = ["index", "name", "tags", "title", "authors", "year"]

# DOI 2 BibTex

BASE_URL = 'http://dx.doi.org/'

# Folders
HOME = expanduser("~")
ARTICLE_SAVE = join(HOME, ".articles")
SAVE_JSON = join(ARTICLE_SAVE, "articles.json")
SETTINGS_JSON = join(ARTICLE_SAVE, "settings.json")
IMAGE_PATH = 'imgs' + sep
LOGO_PATH = join(IMAGE_PATH, 'logo.png')

# Shortcuts
MOVE_RIGHT = 'Ctrl+x'
MOVE_LEFT = 'Ctrl+y'
OPEN_EXPORT = 'Ctrl+e'
QUICK_COPY = 'Ctrl+c'
SHOW_SET = 'Ctrl+q'


SHORTCUTS = {'Move citation to export:': MOVE_RIGHT,
             'Remove citation from export:': MOVE_LEFT,
             'Open the export window:': OPEN_EXPORT,
             'Quick copy a citation:': QUICK_COPY,
             'Show the settings menu:': SHOW_SET}


STANDARD_SETTINGS = {'SIZE_MAIN': (1450, 650),
                     'SIZE_AFK': (50, 50),
                     'BUTTON_COLOR': ("#708090", "#FFFFFF"),
                     'HIDE_EXPLAIN': False,
                     'SHORTCUTS': SHORTCUTS}

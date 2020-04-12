from os.path import expanduser, join, sep

# Constants

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
TITLE_ADD = f'Add an article - {NAME}'
TITLE_EXPORT = 'Export your citations'
TITLE_SETTINGS = f'Settings'
TITLE_CHANGE = f'Change an article'

# Window Sizes

SIZE_ADD = (500, 500)
SIZE_EXP = (400, 650)
SIZE_SET = (400, 650)
SIZE_CHA = (500, 500)

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
GENERAL = join(HOME, ".article_tracker")
ARTICLE_SAVE = join(GENERAL, "articles")
NOTES_PATH = join(GENERAL, 'notes')

SAVE_JSON = join(GENERAL, "articles.json")
SETTINGS_JSON = join(GENERAL, "settings.json")
IMAGE_PATH = 'imgs' + sep
LOGO_PATH = join(IMAGE_PATH, 'logo.png')


# Standard Shortcuts
MOVE_RIGHT = 'Ctrl+x'
OPEN_EXPORT = 'Ctrl+e'
QUICK_COPY = 'Ctrl+c'
SHOW_SET = 'Ctrl+s'
CHANGE_ENT = 'Ctrl+d'
CLOSE_WIND = 'Alt+Escape'
OPEN_NOTE = 'Ctrl+n'


SHORTCUTS = {'Move citation to export:': MOVE_RIGHT,
             'Open the export window:': OPEN_EXPORT,
             'Quick copy a citation:': QUICK_COPY,
             'Show the settings menu:': SHOW_SET,
             'Change entry:': CHANGE_ENT,
             'Close all windows:': CLOSE_WIND,
             'Open notes:': OPEN_NOTE
             }


STANDARD_SETTINGS = {'SIZE_MAIN': (1450, 650),
                     'SIZE_AFK': (50, 50),
                     'BUTTON_COLOR': ("#708090", "#FFFFFF"),
                     'HIDE_EXPLAIN': False,
                     'SHORTCUTS': SHORTCUTS,
                     'NOTES_FORMAT': 'Text'}

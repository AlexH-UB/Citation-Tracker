from os.path import expanduser


# Constants

EXAMPLE_CITATION = '@article{Becker2010,' \
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

VERSION = "beta 1.0"
NAME = f"Alex's Citation Manager Version {VERSION}"
FONT_SIZE = 11

# Window titles

TITLE_MAIN = f'Main Interaction Point - {NAME}'
TITLE_ADD = f'Add a Citation - {NAME}'
TITLE_EXPORT = 'Export your citations'

# Window Sizes

SIZE_MAIN = (1450, 650)
SIZE_ADD = (600, 500)
SIZE_EXP = (400, SIZE_MAIN[1])
SIZE_AFK = (50, 50)

# GUI labels names

LABEL_NAME = 'Label:'
LABEL_TAGS = 'Tags:'
LABEL_BIBTEX = 'BibTex:'
LABEL_TABLE = ["index", "name", "tags", "title", "authors", "year"]

# Color themes

BUTTON_COLOR_THEME1 = ('slategray', 'white')

# Folders
HOME = expanduser("~")
CITATION_SAVE = HOME + "/.citations"
SAVE_JSON = CITATION_SAVE + "/save.json"



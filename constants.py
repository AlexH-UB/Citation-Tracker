from os.path import expanduser
from random import randint


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

r = randint(0, 100)
if r < 33:
    EXAMPLE_CITATION = EXAMPLE_CITATION1
elif 33 <= r < 66:
    EXAMPLE_CITATION = EXAMPLE_CITATION2
else:
    EXAMPLE_CITATION = EXAMPLE_CITATION3


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



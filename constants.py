from os.path import expanduser


# Constants

EXAMPLE_CITATION = '@article{gayvert2016computational, ' \
                   'title={A computational drug repositioning approach for targeting oncogenic transcription factors},' \
                   'author={Gayvert, Kaitlyn M and Dardenne, Etienne and Cheung, Cynthia and Boland, Mary Regina and' \
                   ' Lorberbaum, Tal and Wanjala, Jackline and Chen, Yu and Rubin, Mark A and Tatonetti, Nicholas P and' \
                   'Rickman, David S and others}, journal={Cell reports}, volume={15}, number={11}, ' \
                   'pages={2348--2356}, year={2016}, publisher={Elsevier}}'

VERSION = "beta 1.0"
NAME = f"Alex's Citation Manager Version {VERSION}"
FONT_SIZE = 11

# Window titles

TITLE_MAIN = f'Main Interaction Point - {NAME}'
TITLE_ADD = f'Add a Citation - {NAME}'

# GUI labels names

LABEL_NAME = 'Label:'
LABEL_TAGS = 'Tags:'
LABEL_BIBTEX = 'BibTex:'

# Color themes

BUTTON_COLOR_THEME1 = ('slategray', 'white')

# Folders
HOME = expanduser("~")
CITATION_SAVE = HOME + "/.citations"
SAVE_JSON = CITATION_SAVE + "/save.json"



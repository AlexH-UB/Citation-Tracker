class article:

    def __init__(self, index: int, name: str, path: str, tags: list, access, bibtex: dict, relevance: int):
        """An article is the basic storing unit of the tool.

        :param index: all articles are indexed with numbers in ascending order
        :param name: articles have a short name
        :param path: path to the original file
        :param tags: list with all tags that make it easier to find the documents
        :param access: first access date
        :param bibtex: BibTex citation as dictionary, parsed by BibTex parser module
        :param relevance; How often the article was opened
        """
        self.index = index
        self.name = name
        self.path = path
        self.tags = tags
        self.access = access
        self.bibtex = bibtex
        self.relevance = relevance

    def get_index(self) -> int:
        """Returns the index of the article which is the identifier.
        :return: Index of the article as int
        """
        return self.index

    def get_name(self) -> str:
        """Returns the name of the article given by the user.
        :return: Name of the article as str
        """
        return self.name

    def get_path(self) -> str:
        """Returns the path the article is saved.
        :return: Path of the file as str
        """
        return self.path

    def set_path(self, path: str):
        """Sets the path the article is saved in.
        :param path: Absolute file path of the article
        :return: Nothing
        """
        self.path = path

    def get_tags(self) -> list:
        """Returns all tags of the article given by the user.
        :return: List of all tags provided by the user
        """
        return self.tags

    def get_bibtex(self) -> dict:
        """Returns the BibTex citation of an artivle
        :return: BibTex dictionary of an article
        """
        return self.bibtex

    def get_relevance(self) -> int:
        """Returns the number of opens for the article
        :return: Number the article was opened
        """
        return self.relevance

    def increase_relevance(self):
        """Increases the relevance by 1
        :return: Nothing
        """
        self.relevance += 1

    def get_dict(self) -> dict:
        """ Returns a dictionary with all information of the article.
        :return: dictionary with all information available in a article
        """
        return {'id': self.index,
                'name': self.name,
                'path': self.path,
                'tags': self.tags,
                'access': self.access,
                'bibtex': self.bibtex,
                'relevance': self.relevance
                }

    def bibtex_to_string(self) -> str:
        """Converts the BibTex information stored in an article object to a BibTex string that can be copied or saved as
        .bib file.
        :return: BibTex confirm string
        """
        # Copy the BibTex dictionary
        bib = dict(self.bibtex)
        first = f'@{bib["ENTRYTYPE"]}{{ {bib["ID"]},\n\t'
        del bib['ENTRYTYPE']
        del bib['ID']
        for key, value in bib.items():
            first += f'{key} = {{{value}}}, \n\t'
        first = first[:-4]
        first += ' }'
        return first

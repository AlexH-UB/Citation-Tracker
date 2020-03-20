
class citation:

    def __init__(self,index: int, name: str, path: str, tags: list, access, bibtex: dict):
        """A citation is the basic storing unit of the tool.

        :param index: all citations are indexed with numbers in ascending order
        :param name: citations have a short name
        :param path: path to the original file
        :param tags: list with all tags that make it easier to find the documents
        :param access: first access date
        :param bibTex: BibTex citation as dictionary, parsed by BibTex parser module
        """
        self.index = index
        self.name = name
        self.path = path
        self.tags = tags
        self.access = access
        self.bibtex = bibtex

    def get_index(self) -> int:
        return self.index

    def get_name(self) -> str:
        return self.name

    def get_path(self) -> str:
        return self.path

    def set_path(self, path):
        self.path = path

    def get_tags(self) -> list:
        return self.tags

    def get_bibtex(self) -> dict:
        return self.bibtex

    def get_dict(self) -> dict:
        """ Returns a dictionary with all information of the citation

        :return: dict
        """
        return {'id': self.index,
                'name': self.name,
                'path': self.path,
                'tags': self.tags,
                'access': self.access,
                'bibtex': self.bibtex,
                }

    def bibtex_to_string(self) -> str:
        bib = dict(self.bibtex)
        first = f'@{bib["ENTRYTYPE"]}{{ {bib["ID"]},\n\t'
        del bib['ENTRYTYPE']
        del bib['ID']
        for key, value in bib.items():
            first += f'{key} = "{value}", \n\t'
        first = first[:-4]
        first += ' }'
        return first

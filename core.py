
class citation:

    def __init__(self, index: int, name: str, path: str, tags: list, access, bibTex: dict):
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
        self.bibTex = bibTex

    def get_index(self) -> int:
        return self.index

    def get_name(self) -> str:
        return self.name

    def get_path(self) -> str:
        return self.path

    def get_tags(self) -> list:
        return self.tags

    def get_bibtex(self) -> dict:
        return self.bibTex

    def get_dict(self) -> dict:
        """ Returns a dictionary with all information of the citation

        :return: dict
        """
        return {'id': self.index,
                'name': self.name,
                'path': self.path,
                'tags': self.tags,
                'access:': self.access,
                'latex': self.bibTex,
                }

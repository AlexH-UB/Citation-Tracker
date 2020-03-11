

class citation:

    def __init__(self, number, name, path, tags, access, latex, version=1):
        self.number = number
        self.name = name
        self.path = path
        self.tags = tags
        self.access = access
        self.latex = latex
        self.version = version

    def to_dict(self):
        return {'id': self.number,
                'name': self.name,
                'path': self.path,
                'tags': self.tags,
                'access:': self.access,
                'latex': self.latex,
                'version': self.version}
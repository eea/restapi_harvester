class Loader:
    def read(self, identifier):
        raise NotImplemented


class FSLoader(Loader):
    def read(self, identifier):
        with open(identifier) as f:
            return f.read()

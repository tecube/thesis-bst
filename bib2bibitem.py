class Article:
    def __init__(self):
        self.author
        self.title
        self.journal

class Book:
    pass


class Bibfile:
    def __init__(self):
        pass

    def load(self, path: str):
        pass


class Generator:
    def __init__(self):
        pass
    
    def generate(self):
        bibfile = Bibfile()
        entries = bibfile.load(filename)

        output = ''
        for entry in entries:
            output += entry.to_bibitem()

        print(output)


if __name__ == '__main__':
    g = Generator()
    g.generate()
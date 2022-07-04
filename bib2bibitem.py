import re

class Article:
    def __init__(self, parsed_dict):
        self.citekey = parsed_dict['citekey']
        self.author = parsed_dict['tags']['author'] if 'author' in parsed_dict['tags'] else ["NoName"]
        self.title = parsed_dict['tags']['title'] if 'title' in parsed_dict['tags'] else ""
        self.journal = parsed_dict['tags']['journal'] if 'journal' in parsed_dict['tags'] else ""
        self.year = parsed_dict['tags']['year'] if 'year' in parsed_dict['tags'] else ""
        self.volume = parsed_dict['tags']['volume'] if 'volume' in parsed_dict['tags'] else ""
        self.number = parsed_dict['tags']['number'] if 'number' in parsed_dict['tags'] else ""
        self.pages = parsed_dict['tags']['pages'] if 'pages' in parsed_dict['tags'] else ""

    def to_bibitem(self) -> str:
        bibitem_text = ""
        bibitem_text += "\\bibitem{" + self.citekey + "} " 
        for auth in self.author:
            bibitem_text += auth + ", "
        bibitem_text += "``" + self.title + ",'' " if self.title != "" else ""
        bibitem_text += "\\textit{" + self.journal + "}, " if self.journal != "" else "" #\textit{}はアルファベットのみ対応なので日本語は変化しないはず
        bibitem_text += "Vol. " + self.volume + ", " if self.volume != "" else ""
        bibitem_text += "No. " + self.volume + ", " if self.volume != "" else ""
        if re.search(r"[0-9]\-[0-9]", self.pages):
            bibitem_text += "pp. " + self.pages.replace('-', '--') + " "
        elif re.search("--", self.pages):
            bibitem_text += "pp. " + self.pages + " "
        else:
            bibitem_text += "p. " + self.pages + " " if self.pages != "" else ""
        bibitem_text += "(" + self.year + ")" if self.year != "" else ""
        bibitem_text += "\n"
        return bibitem_text

class Book:
    def __init__(self, parsed_dict):
        self.citekey = parsed_dict['citekey']
        self.author = parsed_dict['tags']['author'] if 'author' in parsed_dict['tags'] else ["NoName"]
        self.title = parsed_dict['tags']['title'] if 'title' in parsed_dict['tags'] else ""
        self.journal = parsed_dict['tags']['journal'] if 'journal' in parsed_dict['tags'] else ""
        self.year = parsed_dict['tags']['year'] if 'year' in parsed_dict['tags'] else ""
        self.pages = parsed_dict['tags']['pages'] if 'pages' in parsed_dict['tags'] else ""
    
    def to_bibitem(self) -> str:
        bibitem_text = ""
        bibitem_text += "\\bibitem{" + self.citekey + "} "
        for auth in self.author:
            bibitem_text += auth + ", "
        bibitem_text += "``" + self.title + ",'' " if self.title != "" else ""
        bibitem_text += self.journal + " " if self.journal != "" else ""
        bibitem_text += "(" + self.year + "), " if self.year != "" else ""
        if re.search(r"[0-9]\-[0-9]", self.pages):
            bibitem_text += "pp. " + self.pages.replace('-', '--') + " "
        elif re.search("--", self.pages):
            bibitem_text += "pp. " + self.pages + " "
        else:
            bibitem_text += "p. " + self.pages + " " if self.pages != "" else ""
        bibitem_text += "\n"
        return bibitem_text


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
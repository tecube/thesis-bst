import argparse
import pathlib
import re
import sys
from bibparser import ParserInput, ParsedEntry, bibfile


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('bibfile', type=str, help='path to the .bib file to be converted')
    parser.add_argument('-o', '--output', type=str, help='path to the output .tex file (just a snippet supposed to be used with "\\input{}" command in the main tex file)')
    return parser.parse_args()


class EntryFormatter: # just for typing (grouping)
    pass


class Article(EntryFormatter):
    def __init__(self, ent: ParsedEntry):
        self.citekey = ent.citekey
        self.author = ent.tags['author'] if 'author' in ent.tags else ""
        self.title = ent.tags['title'] if 'title' in ent.tags else ""
        self.journal = ent.tags['journal'] if 'journal' in ent.tags else ""
        self.year = ent.tags['year'] if 'year' in ent.tags else ""
        self.volume = ent.tags['volume'] if 'volume' in ent.tags else ""
        self.number = ent.tags['number'] if 'number' in ent.tags else ""
        self.pages = ent.tags['pages'] if 'pages' in ent.tags else ""
        self._split_authors()

    def _split_authors(self):
        self.author = self.author.split(' and ')

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


class Book(EntryFormatter):
    def __init__(self, ent: ParsedEntry):
        self.citekey = ent.citekey
        self.author = ent.tags['author'] if 'author' in ent.tags else ["NoName"]
        self.title = ent.tags['title'] if 'title' in ent.tags else ""
        self.publisher = ent.tags['publisher'] if 'publisher' in ent.tags else ""
        self.year = ent.tags['year'] if 'year' in ent.tags else ""
        self.pages = ent.tags['pages'] if 'pages' in ent.tags else ""
        self._split_authors()

    def _split_authors(self):
        self.author = self.author.split(' and ')

    def to_bibitem(self) -> str:
        bibitem_text = ""
        bibitem_text += "\\bibitem{" + self.citekey + "} "
        for auth in self.author:
            bibitem_text += auth + ", "
        bibitem_text += "``" + self.title + ",'' " if self.title != "" else ""
        bibitem_text += self.publisher + " " if self.publisher != "" else ""
        bibitem_text += "(" + self.year + "), " if self.year != "" else ""
        if re.search(r"[0-9]\-[0-9]", self.pages):
            bibitem_text += "pp. " + self.pages.replace('-', '--') + " "
        elif re.search("--", self.pages):
            bibitem_text += "pp. " + self.pages + " "
        else:
            bibitem_text += "p. " + self.pages + " " if self.pages != "" else ""
        bibitem_text += "\n"
        return bibitem_text


def instantiate_formatters(entries: list[ParsedEntry]):
    entry_class: dict[str, EntryFormatter] = {
        'article': Article,
        'book': Book,
    }

    instances: list[EntryFormatter] = []
    for ent in entries:
        inst = entry_class[ent.entry_type](ent)
        instances.append(inst)

    return instances


def str_from_file(filepath: pathlib.Path):
    # assuming the file is not too large
    with open(filepath, mode='r', encoding='utf-8') as f:
        all_content = f.read()
    return all_content


def parse(bibfile_path: pathlib.Path):
    bib = str_from_file(bibfile_path)
    src = ParserInput(bib)

    entries = bibfile(src)

    return instantiate_formatters(entries)


def generate(formatters: list[EntryFormatter], outputfile):
    for ent in formatters:
        print(ent.to_bibitem(), file=outputfile)


if __name__ == '__main__':
    args = get_args()
    bibfile_path = pathlib.Path(args.bibfile)

    if args.output is None:
        output_file = sys.stdout
    else:
        output_file = open(args.output, mode='a', encoding='utf-8') # assuming the file is closed when the program terminates

    formatters = parse(bibfile_path)
    generate(formatters, output_file)

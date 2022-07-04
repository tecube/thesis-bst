from bib_parser import ParserInput, bibfile


class Article:
    def __init__(self, parsed_dict):
        self.author = parsed_dict['tags']['author']
    
    def to_bibitem() -> str:
        return bibitem_text

class Book:
    pass


def instantiate_entries(entries: list[dict]):
    entry_class = {
        'article': Article,
        'book': Book,
    }

    instances = []
    for ent in entries:
        inst = entry_class[ent['entry_type']](ent)
        instances.append(inst)
    
    return instances


def generate():
    bibfile_path = 'test.bib'

    src = ParserInput(src_path=bibfile_path)
    entries = bibfile(src)

    entries = instantiate_entries(entries)

    for ent in entries:
        print(ent)


if __name__ == '__main__':
    generate()
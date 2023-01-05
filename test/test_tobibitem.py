import bib2bibitem

if __name__ == '__main__':
    parsed_dict = {'entry_type': 'article', 'citekey': 'brezis93:_leapf_inter_compet', 'tags': {'author': ['Elise S. Brezis and Paul R. Krugman and Daniel Tsiddon'], 'number': '1', 'title': 'TITLE', 'journal': 'JOURNAL', 'volume': 'VOLUME', 'number': 'NUMBER', 'year': 'YEAR'}}

    if parsed_dict['entry_type'] == 'article':
        article1 = bib2bibitem.Article(parsed_dict)
    elif parsed_dict['entry_type'] == 'book':
        book1 = bib2bibitem.Book(parsed_dict)
    
    print(article1.to_bibitem())
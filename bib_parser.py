from typing import Any, Callable


class ParserInput:
    def __init__(self, src_str: str=None, src_path: str=None):
        if src_str is None and src_path is None:
            raise ValueError('input must be specified as a string or a filename.')
        
        elif src_str is not None:
            self.load_from_str(src_str)
        
        elif src_path is not None:
            self.load_from_file(src_path)
        
        else: # never enter
            pass
    
    def load_from_file(self, path: str):
        with open(path, mode='r') as f:
            all_content = f.read()
        
        self.src = all_content
        self.pos = 0
    
    def load_from_str(self, s: str):
        self.src = s
        self.pos = 0
    
    def next(self, n: int): # just peak, not pop (use pop(n) to consume the n characters)
        slice = self.src[self.pos:self.pos+n]
        if slice == '': # EOF
            raise EOFError('Parser reached the end of the input string.')
        return slice
    
    def pop(self, n: int):
        self.pos += n


#########################
# higher-order functions
#########################

def char_seq(s: str):
    l = len(s)

    def parser_func(src: ParserInput):
        if src.next(l) == s:
            src.pop(l)
            return s
        else:
            raise ValueError(f'Error in parsing "seq({s})": {src.next(10)} not starts with "{s}".')
    
    return parser_func


def parser_seq(parser_func_list: list[Callable[[ParserInput,], Any]]):
    def new_parser_func(src: ParserInput):
        out_seq = []
        for parser in parser_func_list:
            out = parser(src)
            out_seq.append(out)
        return out_seq
    
    return new_parser_func


def many(parser_func: Callable[[ParserInput,], str]):
    def new_parser_func(src: ParserInput):
        seq: str = ''
        try:
            while True:
                seq += parser_func(src)
        except ValueError:
            pass
        return seq

    return new_parser_func


def many1(parser_func: Callable[[ParserInput,], str]):
    def new_parser_func(src: ParserInput):
        seq: str = parser_func(src)
        seq += many(parser_func)(src)
        return seq

    return new_parser_func


def oneof(parser_func_list: list[Callable[[ParserInput,], str]]):
    def new_parser_func(src: ParserInput):
        for parser in parser_func_list:
            try:
                parsed = parser(src)
                break
            except ValueError:
                continue
        else:
            raise ValueError('Erro in parsing with "oneof": no match in the parser list.')
        return parsed

    return new_parser_func


def zero_or_one(parser_func: Callable[[ParserInput,], str]):
    def new_parser_func(src: ParserInput):
        try:
            return parser_func(src)
        except ValueError:
            return ''
    
    return new_parser_func


#######################
# parsers
#######################

def whitespace(src: ParserInput):
    c = src.next(1)
    if c in ' \t\n\r':
        src.pop(1)
        return c
    else:
        raise ValueError(f'Error in parsing "whitespace": {c} is not a whitespace.')


def alphabet(src: ParserInput):
    c = src.next(1)
    if c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        src.pop(1)
        return c
    else:
        raise ValueError(f'Error in parsing "alphabet": {c} is not an alphabet.')


def digit(src: ParserInput):
    c = src.next(1)
    if c in '0123456789':
        src.pop(1)
        return c
    else:
        raise ValueError(f'Error in parsing "digit": {c} is not a digit.')


def punctuation(exclude: str=''):
    def parser_func(src: ParserInput):
        c = src.next(1)

        candidates = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
        for i in range(len(exclude)):
            candidates = candidates.replace(exclude[i], '')

        if c in candidates:
            src.pop(1)
            return c
        else:
            raise ValueError(f'Error in parsing "punctuation": {c} is not a punctuation.')

    return parser_func


#######################
# bib-specific parsers
#######################

def entry_type(src: ParserInput):
    etype = many1(alphabet)(src)
    return etype.lower()


def citekey(src: ParserInput):
    ckey = many1(
        oneof([
            alphabet,
            digit,
            char_seq('-'),
            char_seq('_'),
            char_seq(':')
        ])
    )(src)
    return ckey


def braced_string(src: ParserInput):
    braced = ''
    braced += char_seq('{')(src)
    braced += many(oneof([whitespace, alphabet, digit, punctuation(exclude='{}'), braced_string]))(src)
    braced += char_seq('}')(src)
    return braced


def doublequoted_string(src: ParserInput):
    dquoted = ''
    dquoted += char_seq('"')(src)
    dquoted += many(oneof(whitespace, alphabet, digit, punctuation))(src)
    dquoted += char_seq('"')(src)
    return dquoted


def tag(src: ParserInput):
    pair: dict[str, str] = dict()

    many(whitespace)(src)
    name = many1(alphabet)(src)
    many(whitespace)(src)
    char_seq('=')(src)
    many(whitespace)(src)
    value = oneof([braced_string, doublequoted_string, many1(digit)])(src)

    # strip the outermost braces/double-quotations
    if value[0] == '{' or value[0] == '"':
        value = value[1:-1]

    pair[name] = value

    return pair


def entry(src: ParserInput):
    result = {'entry_type': '', 'citekey': '', 'tags': dict()}

    char_seq('@')(src)
    result['entry_type'] = entry_type(src)

    char_seq('{')(src)
    result['citekey'] = citekey(src)
    char_seq(',')(src)

    many(whitespace)(src)

    while True:
        try:
            result['tags'].update(tag(src))
            char_seq(',')(src)
        except ValueError:
            break

    many(whitespace)(src)
    char_seq('}')(src)

    return result


def bibfile(src: ParserInput):
    entries: list[dict] = []
    try:
        while True:
            many(whitespace)(src)
            ent = entry(src)
            entries.append(ent)
            many(whitespace)(src)
    except EOFError:
        pass

    return entries
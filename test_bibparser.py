from __future__ import annotations
from typing import Callable
import pytest
import bibparser
from bibparser import ParserInput


class TestParserInput: # a class just for grouping
    def test_init(self):
        src_str = "test src_str"
        inst = ParserInput(src_str)
        assert inst.src == src_str
        assert inst.pos == 0
    
    def test_re_load_from_str(self):
        first_src_str = "first src_str"
        inst = ParserInput(first_src_str)
        inst.consume(5)
        assert inst.src == first_src_str
        assert inst.pos == 5

        second_src_str = "second src_str"
        inst.load_from_str(second_src_str)
        assert inst.src == second_src_str
        assert inst.pos == 0

    def test_peak_eof(self):
        src_str = "test src_str"
        inst = ParserInput(src_str)

        inst.consume(100)

        with pytest.raises(EOFError):
            inst.peak(1)
    
    def test_peak_retval(self):
        src_str = "test src_str"
        inst = ParserInput(src_str)

        inst.consume(2)

        assert inst.peak(4) == 'st s'


ALL_CHARS = ' \t\n\r' + 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' + '!"#$%&'+"'"+'()*+,-./:;<=>?@[\\]^_`{|}~'
class TestPrimitiveParsers:
    @classmethod
    def is_accepted(cls, parser_func: Callable, src_str: str, expected_retval: str):
        inst = ParserInput('padding' + src_str)
        inst.consume(len('padding'))

        pos_before = inst.pos
        retval = parser_func(inst)
        pos_after = inst.pos

        assert retval == expected_retval
        assert pos_after == pos_before + 1
    
    @classmethod
    def is_rejected(cls, parser_func: Callable, src_str: str):
        inst = ParserInput('padding' + src_str)
        inst.consume(len('padding'))

        pos_before = inst.pos
        with pytest.raises(ValueError):
            parser_func(inst)
        pos_after = inst.pos

        assert pos_after == pos_before
    
    @pytest.mark.parametrize('accepted_char', set(' \t\n\r'))
    def test_whitespace_accepted(self, accepted_char):
        self.is_accepted(bibparser.whitespace, accepted_char, accepted_char)
    
    @pytest.mark.parametrize('rejected_char', set(ALL_CHARS) - set(' \t\n\r'))
    def test_whitespace_rejected(self, rejected_char):
        self.is_rejected(bibparser.whitespace, rejected_char)
    
    @pytest.mark.parametrize('accepted_char', set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    def test_alphabet_accepted(self, accepted_char):
        self.is_accepted(bibparser.alphabet, accepted_char, accepted_char)
    
    @pytest.mark.parametrize('rejected_char', set(ALL_CHARS) - set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    def test_alphabet_rejected(self, rejected_char):
        self.is_rejected(bibparser.alphabet, rejected_char)
    
    @pytest.mark.parametrize('accepted_char', set('0123456789'))
    def test_digit_accepted(self, accepted_char):
        self.is_accepted(bibparser.digit, accepted_char, accepted_char)
    
    @pytest.mark.parametrize('rejected_char', set(ALL_CHARS) - set('0123456789'))
    def test_digit_rejected(self, rejected_char):
        self.is_rejected(bibparser.digit, rejected_char)
    
    @pytest.mark.parametrize('accepted_char', set('!"#$%&'+"'"+'()*+,-./:;<=>?@[\\]^_`{|}~'))
    def test_punctuation_accepted(self, accepted_char):
        self.is_accepted(bibparser.punctuation(), accepted_char, accepted_char)
    
    @pytest.mark.parametrize('rejected_char', set(ALL_CHARS) - set('!"#$%&'+"'"+'()*+,-./:;<=>?@[\\]^_`{|}~'))
    def test_punctuation_rejected(self, rejected_char):
        self.is_rejected(bibparser.punctuation(), rejected_char)

    @pytest.mark.parametrize('accepted_char', set('"#$%&'+"'"+'()*+,-./:;<=>@[\\]^_`{|}~'))
    def test_punctuation_accepted_with_exception(self, accepted_char):
        self.is_accepted(bibparser.punctuation('!?'), accepted_char, accepted_char)
    
    @pytest.mark.parametrize('rejected_char', set(ALL_CHARS) - set('"#$%&'+"'"+'()*+,-./:;<=>@[\\]^_`{|}~'))
    def test_punctuation_rejected_with_exception(self, rejected_char):
        self.is_rejected(bibparser.punctuation('!?'), rejected_char)


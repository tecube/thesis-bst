import filecmp
import bib2bibitem


def test_inout(tmp_path):
    tmp_output_path = tmp_path.joinpath('test_output.tex')

    with open(tmp_output_path, mode='a', encoding='utf-8') as f:
        formatters = bib2bibitem.parse('test/test_input.bib')
        bib2bibitem.generate(formatters, f)

    filecmp.cmp(tmp_output_path, 'test/test_output.tex')
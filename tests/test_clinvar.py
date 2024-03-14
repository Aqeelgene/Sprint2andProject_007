import builtins

import mock
import pytest

from variant_bridge import clinvar


class TestTask3:

    @staticmethod
    def test_cli_input():
        # Mock the built-in `input` function
        with mock.patch.object(
            builtins,
            'input',
            lambda _: 'NM_000088.3:c.589G>T',
        ):
            # Assert the return value
            assert clinvar.cli_input() == 'NM_000088.3:c.589G>T'

    @pytest.mark.parametrize(
        'user_input, request_type, expected_url',
        (
            # Test for `esearch`
            (
                'NM_000088.3:c.589G>T',
                'esearch',
                (
                    'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
                    '?db=clinvar&retmode=json&term=%22NM_000088.3%3Ac.589G%3ET%22'
                ),
            ),
            (
                'NC_000017.10:g.48275363C>A',
                'esearch',
                (
                    'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
                    '?db=clinvar&retmode=json&term=%22NC_000017.10%3Ag.48275363C%3EA%22'
                ),
            ),
            (
                'NG_007400.1:g.8638G>T',
                'esearch',
                (
                    'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
                    '?db=clinvar&retmode=json&term=%22NG_007400.1%3Ag.8638G%3ET%22'
                ),
            ),
            # Test for `esummary`
            (
                '425635',
                'esummary',
                (
                    'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
                    '?db=clinvar&retmode=json&id=425635'
                ),
            ),
        ),
    )
    def test_generate_url(self, user_input, request_type, expected_url):
        url = clinvar.generate_url(user_input, request_type)
        assert url == expected_url

    @staticmethod
    def test_extract_id(esearch_response):
        expected = '786688'
        variant_id = clinvar.extract_id(esearch_response)
        assert variant_id == expected

    @staticmethod
    def test_extract_data(esummary_response):
        expected = 'Benign'
        variant_id = '786688'
        pathogenicity = clinvar.extract_data(esummary_response, variant_id)
        assert pathogenicity == expected

    @staticmethod
    def test_format_data(final_data):
        data = clinvar.format_data('hgvs', 'variant_id', 'pathogenicity')
        assert data == final_data
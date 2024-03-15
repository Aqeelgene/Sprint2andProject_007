# Test_Task2.py

from unittest.mock import patch, Mock
import pytest
import requests
from Project_task2 import (
    fetch_transcript_id,
    extract_hg38_genomic_description,
    get_ensembl_vep_data,
    sanitize_filename,
)


class TestVariantBridge:
    def test_fetch_transcript_id(self):
        # Mocking the response from the requests.get() call
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = '<reference type="str">TRANSCRIPT_ID</reference>'
            mock_get.return_value = mock_response

            # Testing the function
            transcript_id = fetch_transcript_id('GENE_NAME')

            # Assertion
            assert transcript_id == 'TRANSCRIPT_ID'

    def test_extract_hg38_genomic_description(self):
        # Testing with a mock response_text
        response_text = '{"hg38": {"hgvs_genomic_description": "HG38_DESCRIPTION"}}'
        hg38_description = extract_hg38_genomic_description(response_text)
        assert hg38_description == 'HG38_DESCRIPTION'

    def test_get_ensembl_vep_data(self):
        # Mocking the response from the requests.get() call
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'data': 'some_data'}
            mock_get.return_value = mock_response

            # Testing the function
            ensembl_data = get_ensembl_vep_data('HG38_ID')

            # Assertion
            assert ensembl_data == {'data': 'some_data'}

    def test_sanitize_filename(self):
        input_name = "filename with spaces and $pecial characters!?"
        sanitized_name = sanitize_filename(input_name)
        assert sanitized_name == "filename_with_spaces_and_pecial_characters"

if __name__ == '__main__':
    pytest.main()

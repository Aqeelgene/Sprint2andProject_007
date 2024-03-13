import json
import sys
import urllib.parse as urlparser
from pathlib import Path

import requests


def cli_input():
    """Read user input.

    Current function only works with HGVS.
    """
    print(
        'Welcome to VariantBridge + ClinVar!\n\n'
        'Please input the variant in HGVS, e.g.:\n'
        '- NM_000088.3:c.589G>T\n'
        '- NC_000017.10:g.48275363C>A\n'
        '- NG_007400.1:g.8638G>T\n'
    )
    # User input for the variant.
    hgvs = input('Insert variant: ')
    return hgvs


def generate_url(search_param: str, request_type: str='esearch'):
    """Generate a URL to search for the required info.

    :search_param str: User's input of the variant NM-number.
    :request_type str: Defines the type of tool to be used for the search.

    The two types used are `esearch` and `esummary`. Defaults to `esearch`.

    Example URL's:
    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=%22NG_007400.1%3Ag.8638G%3ET%22&retmode=json
    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=425635&retmode=json
    """
    # Make a request to the VariantValidator server with the variant and extension
    query_params = {
        'db': 'clinvar',
        'retmode': 'json',
    }
    if request_type == 'esearch':
        sp = {'term': f'"{search_param}"'}
    elif request_type == 'esummary':
        sp = {'id': f'{search_param}'}
    else:
        print('ERROR: Allowed request types are `esearch` and `esummary`.')
        sys.sxit(1)

    query_params.update(sp)

    # Generate a query string
    query_string = urlparser.urlencode(query_params, doseq=True)
    # Collect the parts to form the url
    url_parts = (
        'https',
        'eutils.ncbi.nlm.nih.gov',
        f'/entrez/eutils/{request_type}.fcgi',
        query_string,
        '',
    )
    # Generate the url
    return urlparser.urlunsplit(url_parts)


def fetch_clinvar(url: str):
    """Request the ClinVar API."""
    response = requests.get(url)
    if not response.ok:
        print(
            'Something is wrong with your request.\n',
            f'Status code: {response.status_code}.\n',
            f'Errors: {response.errors}.'
        )
        sys.exit(1)

    return response.json()


def extract_id(data: dict):
    """Extract variant id from the clinvar reponse."""
    #import pdb;pdb.set_trace()
    variant_id = data.get('esearchresult', {}).get('idlist', [''])[0]
    if variant_id:
        return variant_id

    print('Error: No variant id has been extracted!')
    sys.exit(1)


def extract_data(data: dict, variant_id: int):
    """Extract data of the variant id from the clinvar reponse."""
    result = data.get('result', {}).get(variant_id, {})
    pathogenicity = result.get(
        'germline_classification', {}
    ).get(
        'description', {}
    )
    return pathogenicity


def format_data(hgvs: str, variant_id: int, pathogenicity: str):
    return {
        'HGVS': hgvs,
        'variant_id': variant_id,
        'pathogenicity': pathogenicity,
    }


def save_to_file(data: dict):
    """Save extracted data into a file with a unique name."""
    hgvs = data.get('HGVS')
    valid_chars = f'-_.() {string.ascii_letters}{string.digits}'
    sanitised_name = ''.join(c for c in hgvs if c in valid_chars)
    filename = f'{sanitised_name}_CVar.json'
    with open(filename, 'w') as f:
        json.dump(data, f)

    print(f'Data saved to file {filename}')
    sys.exit(0)


if __name__ == '__main__':
    # Get HGVS from the user
    hgvs = cli_input()
    # Generate the esearch URL
    esearch_url = generate_url(hgvs)
    # Make the request
    esearch_response = fetch_clinvar(esearch_url)
    # Extract variant ID
    variant_id = extract_id(esearch_response)
    # Generate the esummary URL
    esummary_url = generate_url(hgvs, request_type='esummary')
    # Make the request
    esummary_response = fetch_clinvar(esummary_url)
    # Extract data
    pathogenicity = extract_data(esummary_response)
    # Format extracted data
    data = format_data(hgvs, variant_id, pathogenicity)
    # Save the data to file
    save_to_file(data)
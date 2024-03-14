import pytest


@pytest.fixture
def esearch_response():
    return {
        'header': {
            'type': 'esearch',
            'version': '0.3',
        },
        'esearchresult': {
            'count': '1',
            'retmax': '1',
            'retstart': '0',
            'idlist': [
                '786688'
            ],
            'translationset': [],
        },
    }


@pytest.fixture
def esummary_response():
    return {
        'header': {
            'type': 'esummary',
            'version': '0.3',
        },
        'result': {
            '786688': {
                'uid': '786688',
                'obj_type': 'single nucleotide variant',
                'accession': 'VCV000786688',
                'accession_version': 'VCV000786688.',
                'title': 'NM_005239.6(ETS2):c.190G>A (p.Ala64Thr)',
                'variation_set': [
                    {
                        'measure_id': '717204',
                        'variation_xrefs': [
                            {
                                'db_source': 'dbSNP',
                                'db_id': '34373350',
                            },
                        ],
                        'variation_name': 'NM_005239.6(ETS2):c.190G>A (p.Ala64Thr)',
                        'cdna_change': 'c.190G>A',
                        'aliases': [],
                        'allele_freq_set': [
                            {
                                'source': 'The Genome Aggregation Database (gnomAD), exomes',
                                'value': '0.00305',
                                'minor_allele': '',
                            },
                            {
                                'source': 'NHLBI Exome Sequencing Project (ESP) Exome Variant Server',
                                'value': '0.00976',
                                'minor_allele': '',
                            },
                            {
                                'source': '1000 Genomes Project',
                                'value': '0.00859',
                                'minor_allele': 'A',
                            },
                        ],
                        'variant_type': 'single nucleotide variant',
                        'canonical_spdi': 'NC_000021.9:38814277:G:A',
                    },
                ],
                'supporting_submissions': {
                    'scv': [
                        'SCV001116258',
                    ],
                    'rcv': [
                        'RCV000968784',
                    ],
                },
                'germline_classification': {
                    'description': 'Benign',
                    'last_evaluated': '2019/01/01 00:00',
                    'review_status': 'criteria provided, single submitter',
                    'trait_set': [
                        {
                            'trait_xrefs': [
                              {
                                  'db_source': 'MedGen',
                                  'db_id': 'C3661900',
                              },
                            ],
                            'trait_name': 'not provided',
                        },
                    ],
                },
                'clinical_impact_classification': {
                    'description': '',
                    'last_evaluated': '1/01/01 00:00',
                    'review_status': '',
                    'trait_set': [],
                },
                'oncogenicity_classification': {
                    'description': '',
                    'last_evaluated': '1/01/01 00:00',
                    'review_status': '',
                    'trait_set': [],
                },
                'record_status': '',
                'gene_sort': 'ETS2',
                'chr_sort': '21',
                'location_sort': '00000000000038814278',
                'protein_change': 'A204T, A64T',
                'fda_recognized_database': '',
            },
            'uids': [
                '786688',
            ],
        }
    }


@pytest.fixture
def final_data():
    return {
        'HGVS': 'hgvs',
        'variant_id': 'variant_id',
        'pathogenicity': 'pathogenicity',
    }
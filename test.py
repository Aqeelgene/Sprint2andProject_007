import requests
import re
def fetch_transcript_id(gene_name):
    url = f"https://rest.variantvalidator.org/VariantValidator/tools/gene2transcripts_v2/{gene_name}/mane_select/refseq/GRCh37?content-type=text/xml"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data from the server. Status code: {response.status_code}")
        return None

    match = re.search(r'<reference type="str">(.*?)</reference>', response.text)
    return match.group(1) if match else None
trial_run = fetch_transcript_id("BRCA2")
print(trial_run)
NM_000059.4
""" This is the Project_task2.py which is the code following on from
Project_task1.1. To the file Project_task2.py Zahra has updated the code to have
string formatting in order to have dynamic naming and added comments - 28 Feb 2024 """

import requests  #imports the requests library
import json      #import the json module
import string    #import the string module

# Function to sanitize input to use as a valid filename
def sanitize_filename(input_name):
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    sanitized_name = ''.join(c for c in input_name if c in valid_chars)
    return sanitized_name.replace(" ", "_")

# Function to fetch transcript ID using gene name
def fetch_transcript_id(gene_name):
    url = f"https://rest.variantvalidator.org/VariantValidator/tools/gene2transcripts_v2/{gene_name}/mane_select/refseq/GRCh37?content-type=text/xml"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data from the server. Status code: {response.status_code}")
        return None
    match = re.search(r'<reference type="str">(.*?)</reference>', response.text)
    return match.group(1) if match else None

# Function to extract the hg38 genomic description using regex
def extract_hg38_genomic_description(response_text):
    match = re.search(r'"hg38":\s*\{\s*"hgvs_genomic_description":\s*"([^"]+)"', response_text)
    return match.group(1) if match else None

# Function to get data from Ensembl VEP API using hg38 ID
def get_ensembl_vep_data(hg38_id):
    url = f"https://rest.ensembl.org/vep/human/hgvs/{hg38_id}"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching data from Ensembl VEP API. Status code: {response.status_code}")
        return None
    return response.json()

# Main code
server = "https://rest.variantvalidator.org/VariantValidator/variantvalidator/"
print("Welcome to VariantBridge!\n\n"
      "Convert your genetic variants from hg19 to hg38. Please input the variant in HGVS or VCF format (hg19), e.g.:\n"
    "- HGVS: NM_000088.3:c.589G>T\n"
      "- HGVS: NC_000017.10:g.48275363C>A\n"
      "- HGVS: NG_007400.1:g.8638G>T\n"
      "- VCF: 17-50198002-C-A\n"
      "- VCF: 17:50198002:C:A\n"
      "- VCF: chr17:50198002C>A\n"
      "- VCF: chr17:g.50198002C>A\n\n"
      "Please enter your data in one of these formats to proceed with the conversion.")

variant = input("Insert variant:")

# Check if variant starts with 'NM_' or 'NC' or 'NG_'
if variant.startswith(('NM_','NC_','NG_')):
    ext = variant.split(':')[0]  # Use part of the variant before the colon
else:
    gene_name = input("Enter the gene name: ")
    ext = fetch_transcript_id(gene_name)
    if ext is None:
        print("No transcript ID found for the given gene name.")
        exit()

response = requests.get(f"{server}hg19/{variant}/{ext}")
if response.status_code == 200:
    hg38_genomic_description = extract_hg38_genomic_description(response.text)
    print(f"HG38 Genomic Description: {hg38_genomic_description}")
    if hg38_genomic_description:
        ensembl_vep_data = get_ensembl_vep_data(hg38_genomic_description)
        print("Ensembl VEP Data:", ensembl_vep_data)
    else:
        print("No hg38 genomic description found, cannot query Ensembl VEP API.")
else:
    print(f"Error: Received response code {response.status_code}")

# Json output format
decode = response.json()
print(repr(decode))

# Generate file name based on the variant input
fileName = f"{sanitize_filename(variant)}.txt"

if fileName:
    with open(fileName, "w") as file:
        file.write(json.dumps(decode, sort_keys=True, indent=2))
        file.close()

    print(f"Output written to {fileName}")
# Json output format
decode = response.json()
print(repr(decode))

# Generate file name based on the variant input
fileName = f"{sanitize_filename(variant)}.txt"

if fileName:
    with open(fileName, "w") as file:
        file.write(json.dumps(decode, sort_keys=True, indent=2))
        file.close()

    print(f"Output written to {fileName}")






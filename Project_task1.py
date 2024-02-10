import requests
import re
import json

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
      "Convert your genetic variants from hg19 to hg38. Please input the variant in HGVS or VCF format (hg19)")

genome_build = input("Please select the genome build (hg19 or hg38): ")
if genome_build == "hg19":
    server += "hg19/"
elif genome_build == "hg38":
    server += "hg38/"
else:
    print("Invalid genome build selected. Please try again.")
    exit()

variant = input("Please enter your variant in HGVS or VCF format (hg19): ")

# Check if variant starts with 'N'
if variant.startswith('N'):
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

print(response)

# Json output format
decode = response.json()
print(repr(decode))

# Write the json to file
fileName = "output.txt"
#if saveAnnotations:
    #fileName = makeFileName("variant")

if fileName:
    file = open(fileName, "w")
    file.write(json.dumps(decode, sort_keys=True, indent=2))
    file.close()
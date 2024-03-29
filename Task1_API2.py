#This file "Task1_API2" is a follow on from "Task1_API" and was an attempt to create fields to enter the required information.
# I didn't take this any further


import requests
import re
import json
from flask import Flask, request, make_response
from flask_restx import Api, Resource

# Initialize Flask application and Flask-RESTx API
app = Flask(__name__)
api = Api(app)


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


# Namespace for VariantBridge API
variant_bridge_ns = api.namespace('VariantBridge', description='Convert genetic variants from hg19 to hg38')


@variant_bridge_ns.route("/")
class VariantBridge(Resource):
    def get(self):
        genome_build = request.args.get('genome_build', None)

        if not genome_build:
            return {"message": "Please provide the genome_build parameter (hg19 or hg38)."}, 400

        if genome_build not in ["hg19", "hg38"]:
            return {"message": "Invalid genome build selected. Please provide hg19 or hg38."}, 400

        variant = request.args.get('variant', None)

        if not variant:
            return {"message": "Please provide the variant parameter."}, 400

        server = f"https://rest.variantvalidator.org/VariantValidator/variantvalidator/{genome_build}/"

        # Check if variant starts with 'N'
        if variant.startswith('N'):
            ext = variant.split(':')[0]  # Use part of the variant before the colon
        else:
            gene_name = request.args.get('gene_name', None)
            if not gene_name:
                return {"message": "Please provide the gene_name parameter for non-N variants."}, 400

            ext = fetch_transcript_id(gene_name)
            if ext is None:
                return {"message": "No transcript ID found for the given gene name."}, 404

        response = requests.get(f"{server}hg19/{variant}/{ext}")
        if response.status_code == 200:
            hg38_genomic_description = extract_hg38_genomic_description(response.text)
            if hg38_genomic_description:
                ensembl_vep_data = get_ensembl_vep_data(hg38_genomic_description)
                return {"hg38_genomic_description": hg38_genomic_description, "ensembl_vep_data": ensembl_vep_data}, 200
            else:
                return {"message": "No hg38 genomic description found, cannot query Ensembl VEP API."}, 404
        else:
            return {"message": f"Error: Received response code {response.status_code}"}, response.status_code


if __name__ == '__main__':
    app.run(debug=True)
import json
import string
import sys
import urllib.parse as urlparser
import streamlit as st
import requests
import pandas as pd


def cli_input():
    """Read user input.

    Current function only works with HGVS.
    """
    st.title("VariantBridge ClinVar App")
    st.write("Please input the variant(s) in HGVS, separated by commas, e.g.:")
    st.write("NM_000088.3\:c.589G>T, NC_000017.10\:g.48275363C>A, NG_007400.1\:g.8638G>T")

    # User input for the variant(s)
    hgvs_input = st.text_input("Insert variant(s):")
    # Split the input by commas and remove any leading/trailing whitespace
    hgvs_list = [hgvs.strip() for hgvs in hgvs_input.split(",")]
    return hgvs_list


def generate_url(search_param: str, request_type: str = "esearch"):
    """Generate a URL to search for the required info.

    :search_param str: User's input of the variant NM-number.
    :request_type str: Defines the type of tool to be used for the search.
    The two types used are `esearch` and `esummary`. Defaults to `esearch`.

    Example URL's:
    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=%22NG_007400.1%3Ag.8638G%3ET%22&retmode=json
    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=425635&retmode=json
    """
    # Make a request to the ClinVar server
    query_params = {
        "db": "clinvar",
        "retmode": "json",
    }
    if request_type == "esearch":
        sp = {"term": f'"{search_param}"'}
    elif request_type == "esummary":
        sp = {"id": f"{search_param}"}
    else:
        print("ERROR: Allowed request types are `esearch` and `esummary`.")
        sys.exit(1)

    query_params.update(sp)

    # Generate a query string
    query_string = urlparser.urlencode(query_params, doseq=True)
    # Collect the parts to form the url
    url_parts = (
        "https",
        "eutils.ncbi.nlm.nih.gov",
        f"/entrez/eutils/{request_type}.fcgi",
        query_string,
        "",
    )
    # Generate the url
    return urlparser.urlunsplit(url_parts)


def fetch_clinvar(url: str):
    """Request the ClinVar API."""
    response = requests.get(url)
    if not response.ok:
        print(
            "Something is wrong with your request.\n",
            f"Status code: {response.status_code}.\n",
        )
        sys.exit(1)

    return response.json()


def extract_id(data: dict):
    """Extract variant id from the clinvar response."""
    variant_id = data.get("esearchresult", {}).get("idlist", [""])[0]
    if variant_id:
        return variant_id

    print("Error: No variant id has been extracted!")
    sys.exit(1)


def extract_data(data: dict, variant_id: str):
    """Extract data of the variant id from the clinvar response."""

    result = data.get("result", {}).get(variant_id, {})
    pathogenicity = result.get("germline_classification", {}).get("description", "")
    return pathogenicity


def save_to_file(data: dict):
    """Save extracted data into a file with a unique name."""
    hgvs = data.get("HGVS")
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    sanitised_name = "".join(c for c in hgvs if c in valid_chars)
    filename = f"{sanitised_name}_CVar.json"
    with open(filename, "w") as f:
        json.dump(data, f)

    print(f"Data saved to file {filename}")
    sys.exit(0)


def format_data(
    hgvs: str, variant_id: str, pathogenicity: str, esummary_response: dict
):
    return {
        "HGVS": hgvs,
        "variant_id": variant_id,
        "pathogenicity": pathogenicity,
        "esummary_response": esummary_response,
    }


def display_dashboard(data: dict):
    st.header(f"Variant Nomenclature: ")
    st.subheader(data['HGVS'].replace(":", "\:"))
    st.write(f"ClinVar variant ID: {data['variant_id']}")
    st.write(f"Pathogenicity: {data['pathogenicity']}")

    # Display additional information from the esummary response
    result = data["esummary_response"]["result"][data["variant_id"]]
    st.subheader("Variant Details")
    st.write(f"Title: {result['title']}")
    st.write(f"Variant Type: {result['variation_set'][0]['variant_type']}")
    st.write(f"Canonical SPDI: {result['variation_set'][0]['canonical_spdi']}")

    # Display gene information
    gene_info = result["genes"][0]
    st.subheader("Gene Information")
    st.write(f"Gene Symbol: {gene_info['symbol']}")
    st.write(f"Gene ID: {gene_info['geneid']}")
    st.write(f"Strand: {gene_info['strand']}")

    # Display variation locations in a table
    loc_data = []
    for loc in result["variation_set"][0]["variation_loc"]:
        loc_data.append(
            {
                "Assembly Name": loc["assembly_name"],
                "Chromosome": loc["chr"],
                "Band": loc["band"],
                "Start": loc["start"],
                "Stop": loc["stop"],
            }
        )
    loc_df = pd.DataFrame(loc_data)
    st.subheader("Variation Locations")
    st.table(loc_df)


if __name__ == "__main__":
    # Store the data for each variant
    variant_data = []

    # Get HGVS from the user
    hgvs_list = cli_input()
    for hgvs in hgvs_list:
        if hgvs:
            # Generate the esearch URL
            esearch_url = generate_url(hgvs)
            # Make the request
            esearch_response = fetch_clinvar(esearch_url)
            # Extract variant ID
            variant_id = extract_id(esearch_response)
            # Generate the esummary URL
            esummary_url = generate_url(variant_id, request_type="esummary")
            # Make the request
            esummary_response = fetch_clinvar(esummary_url)
            # Extract data
            pathogenicity = extract_data(esummary_response, variant_id)
            # Format extracted data
            data = format_data(hgvs, variant_id, pathogenicity, esummary_response)
            # Add the data to the list
            variant_data.append(data)
            # Display the detailed dashboard for the variant
            display_dashboard(data)

    # Display the summary table for all variants
    st.header("Variant Summary")
    summary_data = []
    for data in variant_data:
        gene_symbol = data["esummary_response"]["result"][data["variant_id"]]["genes"][0]["symbol"]
        summary_data.append({
            "HGVS": data["HGVS"],
            "Variant ID": data["variant_id"],
            "Gene Symbol": gene_symbol,
            "Pathogenicity": data["pathogenicity"]
        })
    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)

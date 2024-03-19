# ClinVar +Variant Bridge Dashboard

This Python script creates a Streamlit dashboard that allows users to input one or more variants in HGVS format and retrieve relevant information from the ClinVar database. The dashboard displays detailed information for each variant and provides a summary table of all the variants at the end.

## Requirements

- Python 3.10 or higher
- Streamlit
- Requests
- Pandas

You can install the required libraries using pip:

```
pip install -r requirements.txt 
```

## Usage

1. Clone the repository or download the script file.

2. Open a terminal or command prompt and navigate to the directory where the script is located.

3. Run the script using Streamlit:

```
streamlit run clinvar.py
```

Replace `clinvar.py` with the actual name of the script file.

4. The Streamlit app will open in your default web browser.

5. Enter the variant(s) in HGVS format, separated by commas, in the text input field.Note:different gene variants can be also typed in the text input field
```
NM_000088.3:c.589G>T, NC_000017.10:g.48275363C>A, NG_007400.1:g.8638G>T
```

6. Press Enter or click outside the text input field to submit the variants.

7. The dashboard will display the detailed information for each variant, including:
   - Variant Information (HGVS, Variant ID, Pathogenicity)
   - Variant Details (Title, Variant Type, Canonical SPDI)
   - Gene Information (Gene Symbol, Gene ID, Strand)
   - Variation Locations (Assembly Name, Chromosome, Band, Start, Stop)
   - Molecular Consequences (Bar chart showing the count of each consequence)

8. After displaying the detailed information for all variants, a summary table will be shown at the end, containing the HGVS, Variant ID, and Pathogenicity for each variant.

## Script Details

The script consists of several functions that perform different tasks:

- `cli_input()`: Reads user input for the variant(s) in HGVS format.
- `generate_url()`: Generates a URL to search for the required information in the ClinVar database.
- `fetch_clinvar()`: Sends a request to the ClinVar API and retrieves the response.
- `extract_id()`: Extracts the variant ID from the ClinVar response.
- `extract_data()`: Extracts the pathogenicity data for the variant ID from the ClinVar response.
- `format_data()`: Formats the extracted data into a dictionary.
- `save_to_file()`: Saves the extracted data to a JSON file (not used in the current version of the script).
- `display_dashboard()`: Displays the detailed information for a variant on the Streamlit dashboard.

The script starts by calling the `cli_input()` function to get the variant(s) from the user. It then iterates over each variant and performs the following steps:

1. Generates the esearch URL and retrieves the response from ClinVar.
2. Extracts the variant ID from the esearch response.
3. Generates the esummary URL using the variant ID and retrieves the response from ClinVar.
4. Extracts the pathogenicity data from the esummary response.
5. Formats the extracted data into a dictionary.
6. Appends the formatted data to the `variant_data` list.
7. Displays the detailed information for the variant on the dashboard using the `display_dashboard()` function.

After processing all variants, the script displays a summary table containing the HGVS, Variant ID, and Pathogenicity for each variant.

# References used for ClinVar Dashboard 

## ClinVar Key References

1. [Accessing and using data from ClinVar](https://ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/#api)
2. [Identifiers in ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/docs/identifiers/)
3. [Guide to using files from the ftp site or accessed via e-utilities](https://www.ncbi.nlm.nih.gov/clinvar/docs/ftp_primer/)
4. [ClinVar Example Variant Accession](https://www.ncbi.nlm.nih.gov/clinvar/variation/12347/)
5. [ClinVar API help](https://www.biostars.org/p/9496513/)
6. [Get ClinVar info for SNP with VEP](https://www.biostars.org/p/438518/)

## Streamlit GUI Key References

7. [Streamlit Documentation](https://docs.streamlit.io/)
8. [Streamlit Library API Reference](https://docs.streamlit.io/library/api-reference)
9. [How to Build a Streamlit App (Beginner level Streamlit tutorial) - Part 1](https://www.youtube.com/watch?v=-IM3531b1XU&list=PLM8lYG2MzHmRpyrk9_j9FW0HiMwD9jSl5&index=1&ab_channel=M%C4%B1sraTurp)
10. [How to Collect User Input with Streamlit - Part 2](https://www.youtube.com/watch?v=QetpwPnEpgA&list=PLM8lYG2MzHmRpyrk9_j9FW0HiMwD9jSl5&index=2&ab_channel=M%C4%B1sraTurp)
11. [How to Integrate Machine Learning to Streamlit - Part 3](https://www.youtube.com/watch?v=CSv2TBA9_2E&list=PLM8lYG2MzHmRpyrk9_j9FW0HiMwD9jSl5&index=3&ab_channel=M%C4%B1sraTurp)
12. [How to Deploy a Streamlit App - Part 4](https://www.youtube.com/watch?v=B0MUXtmSpiA&list=PLM8lYG2MzHmRpyrk9_j9FW0HiMwD9jSl5&index=4&ab_channel=M%C4%B1sraTurp)
13. [Streamlit Elements You Should Know About in 2023](https://www.youtube.com/watch?v=_Um12_OlGgw&ab_channel=M%C4%B1sraTurp)
14. [Guide to writing on Readme.md (.markdown) file for GitHub project](https://abhiappmobiledeveloper.medium.com/guide-to-writing-on-readme-md-markdown-file-for-github-project-8aad4e4e2a15#:~:text=When%20you%20create%20a%20repository,which%20stands%20for%20Markdown%20documentation)
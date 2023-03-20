'''
This script is searching for "Autorizatii de construire" from Primaria sector 3 website
'''
import re
import requests
from io import BytesIO
from PyPDF2 import PdfReader
import json
import os
import config


for x in range(1, 13):
    ac_file = f'AC_2023_{x}.pdf'
    if not os.path.exists(ac_file) or (os.path.exists(ac_file) and os.path.getsize(ac_file) == 0):
        # PDF file from a URL
        url = f'https://www.primarie3.ro/images/uploads/formulare/{ac_file}'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for any errors in the response
        except requests.exceptions.RequestException as e:
            if response.status_code != 404:
                print(f'An error occurred: {e}')
            continue

        print(f"Downloaded {ac_file}...")
        with open(ac_file, 'wb') as f:
            f.write(response.content)
        pdf_file = BytesIO(response.content)

    else:
        with open(ac_file, 'rb') as f:
            pdf_file = BytesIO(f.read())

    # open the PDF file and search for a number in the last column of a table
    pdf_reader = PdfReader(pdf_file)

    all_rows = {}
    j = 0
    header = 0
    # define the regular expression to match the start of each row
    row_regex = re.compile(r'\d+\s+\d{2}\.\d{2}\.\d{4}')

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        rows = page_text.split('\n')  # split the text into rows
        for i, row in enumerate(rows):
            # print(i, row)
            if header == 0:  # skipping the table header
                header = 1
                continue

            if row_regex.match(row):  # check if the row starts with a number and a date
                j += 1
                all_rows[j] = ""
                row = re.sub('\d+ ', '', row)  # remove the ID
                row = re.sub(r'(\d{2}\.\d{2}\.\d{4})', r'\1 ', row)  # add a space after the date

            # row = re.sub(r'(\d{6})$', r' \1 \n', row)  # add a space before the cadastral number
            all_rows[j] += row

    for search in config.search_terms.keys():
        print(f"Looking inside {ac_file} for {search}: {config.search_terms[search]}")
        values = [value for value in all_rows.values() if search in value]
        if values:
            print(values)

    # json_object = json.dumps(all_rows, indent=4)
    # print(json_object)

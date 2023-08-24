import re
import requests
from io import BytesIO
from PyPDF2 import PdfReader
import os
import config


def download_pdf(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        if response.status_code != 404:
            print(f'An error occurred: {e}')
        return None

    full_path = os.path.join('downloads', filename)

    with open(full_path, 'wb') as f:
        f.write(response.content)

    print(f"Downloaded {filename}...")
    return BytesIO(response.content)


for year in config.years:
    # skip older PDFs since the newer one already has that information
    skip_ac_older_pdfs_for_year = False
    skip_cu_older_pdfs_for_year = False

    for x in reversed(range(1, 13)):
        # AC
        if skip_ac_older_pdfs_for_year:
            continue

        ac_file_name = f'AC_{year}_{x}.pdf'
        ac_file = os.path.join('downloads', ac_file_name)

        if not os.path.exists(ac_file) or (os.path.exists(ac_file) and os.path.getsize(ac_file) == 0):
            ac_url = f'https://www.primarie3.ro/images/uploads/formulare/{ac_file}'
            ac_pdf_file = download_pdf(ac_url, ac_file)
            print(f"Trying to download {ac_file} since it doesn't exists locally...")
        else:
            with open(ac_file, 'rb') as f_ac:
                print(f"Open local file {ac_file}!")
                ac_pdf_file = BytesIO(f_ac.read())

        # open the PDF file and search for a number in the last column of a table
        if ac_pdf_file:
            try:
                ac_pdf_reader = PdfReader(ac_pdf_file)
            except Exception:
                print(f"Cannot open {ac_pdf_file}!")

            skip_ac_older_pdfs_for_year = True

            all_rows = {}
            j = 0
            header = 0
            # define the regular expression to match the start of each row
            row_regex = re.compile(r'\d+\s+\d{2}\.\d{2}\.\d{4}')

            for page in ac_pdf_reader.pages:
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

                    all_rows[j] += row

            for search in config.search_terms.keys():
                print(f"Looking inside {ac_file} for {search}: {config.search_terms[search]}")
                values = [value for value in all_rows.values() if search in value]
                if values:
                    print(values)

        # CU
        print()
        if skip_cu_older_pdfs_for_year:
            continue

        cu_file_name = f'CU_{year}_{x}.pdf'
        cu_file = os.path.join('downloads', cu_file_name)

        if not os.path.exists(cu_file) or (os.path.exists(cu_file) and os.path.getsize(cu_file) == 0):
            cu_url = f'https://www.primarie3.ro/images/uploads/formulare/{cu_file}'
            cu_pdf_file = download_pdf(cu_url, cu_file)
        else:
            with open(cu_file, 'rb') as f_cu:
                cu_pdf_file = BytesIO(f_cu.read())

        if cu_pdf_file:
            try:
                cu_pdf_reader = PdfReader(cu_pdf_file)
            except Exception:
                print(f"Cannot open {cu_pdf_file}!")

            skip_cu_older_pdfs_for_year = True

            all_rows = {}
            j = 0
            header = 0

            for page in cu_pdf_reader.pages:
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

                    all_rows[j] += row

            for search in config.search_terms.keys():
                print(f"Looking inside {cu_file} for {search}: {config.search_terms[search]}")
                values = [value for value in all_rows.values() if search in value]
                if values:
                    print(values)

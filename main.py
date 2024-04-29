import csv_from_ical as csv
import html_invoice as h
import asyncio
import os
from html_to_pdf import generate_pdf_from_html



#Takes information from fscoachristina@gmail.com.ics and makes individual csv files for each student using csv_from_ical.py

ecal = csv.read_calendar('fscoachchristina@gmail.com.ics')
invoices = csv.generate_invoices(ecal, csv.STUDENT_NAMES)
csv_files = csv.write_invoices_to_csv(invoices, csv.STUDENT_NAMES)
month_total = csv.list_of_totals(invoices, csv.STUDENT_NAMES)
print(month_total)

#Takes csv files and converts them to a stylized html

h.convert_csv_to_html( h.folder_path, h.output_folder)

#takes converts html to pdf

async def main():
    folder_path = 'html_invoices/'

    # Ensure the output directory exists
    output_folder = 'pdf_invoices/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            html_file_path = os.path.join(folder_path, filename)
            pdf_file_path = os.path.join(output_folder, f'invoice_{os.path.splitext(filename)[0]}.pdf')

            with open(html_file_path, "r") as file:
                html_content = file.read()

            await generate_pdf_from_html(html_content, pdf_file_path)

# Run the main coroutine
asyncio.run(main())

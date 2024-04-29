import asyncio
from pyppeteer import launch
import os


async def generate_pdf_from_html(html_content, pdf_path):
    browser = await launch()
    page = await browser.newPage()

    await page.setContent(html_content)

    await page.pdf({'path': pdf_path, 'format': 'A4'})

    await browser.close()


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

import pandas as pd
import os

def generate_html_invoice(csv_file):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Calculate total charge
    total = round(df['Charge'].sum(), 2)

    # Generate HTML string for the invoice
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Invoice</title>
    <style>
    body {{
        font-family: Arial, sans-serif;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }}
    .invoice-container {{
        width: 600px;
        margin: 40px auto 0 auto; /* Adjusted margin-top to 40px */
        padding: 40px;
        background-color: #f4f4f4;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .invoice-header {{
        text-align: center;
        margin-bottom: 40px;
    }}
    .invoice-table {{
        width: 100%;
        border-collapse: collapse;
    }}
    .invoice-table th, .invoice-table td {{
        border: 1px solid #e0e0e0;
        padding: 12px;
        text-align: left;
        font-size: 14px;
    }}
    .invoice-table th {{
        background-color: #f8f8f8;
        font-weight: bold;
    }}
    .total-row {{
        background-color: #ffffff;
    }}
    .total-row .total-label {{
        text-align: right;
    }}
    .total-row .total-amount {{
        text-align: right;
        font-weight: bold;
    }}
    </style>
    </head>
    <body>
    <div class="invoice-container">
        <div class="invoice-header">
            <h1>Invoice</h1>
            <h2>Figure Skating Lessons</h2>
        </div>
        <table class="invoice-table">
          <tr>
            <th>Date</th>
            <th>Student</th>
            <th>Lesson Length</th>
            <th>Charge</th>
          </tr>
    """

    # Add rows for each entry in the DataFrame
    for index, row in df.iterrows():
        html += f"<tr><td>{row['Date']}</td><td>{row['Student']}</td><td>{row['Lesson Length']}</td><td>${row['Charge']}</td></tr>"

    # Add a separate row for the Total
    html += f"""
        <tr class='total-row'>
            <td class='total-label' colspan='3'>Total:</td>
            <td class='total-amount'>${total}</td>
        </tr>
    """

    # Close HTML tags
    html += """
        </table>
    </div>
    </body>
    </html>
    """

    return html


# Example usage


# Write HTML content to a file

folder_path = 'Invoices/'
output_folder = 'html_invoices'

def convert_csv_to_html(folder_path, output_folder):
    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            csv_file = os.path.join(folder_path, filename)
            html_content = generate_html_invoice(csv_file)
            with open(os.path.join(output_folder, f'invoice_{os.path.splitext(filename)[0]}.html'), 'w') as file:
                file.write(html_content)
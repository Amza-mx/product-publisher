# Script that retrieves product information using data from both Google Sheets and the Keepa API,
# and then writes the consolidated product details to a CSV file.
# Workflow:
# 1. Fetch a list of ASINs from a specified Google Sheets document.
# 2. Limit the ASIN list to the first 20 entries.
# 3. Process ASINs in batches of 5:
#     a. Retrieve product data from the Keepa API for the US domain.
#     b. Retrieve product data from the Keepa API for the MX domain.
#     c. Extract product details (ASIN, title, brand, category, description, and price) for both domains.
#     d. Combine the extracted data from US and MX into a unified format.
# 4. Write the compiled data into a CSV file named 'products.csv' with predefined headers.
# Dependencies:
# - integrations.KeepaAPI: For interfacing with the Keepa API to obtain product data.
# - integrations.GoogleSheetsAPI: For extracting ASINs from a Google Sheets document.
# - config.settings: Provides configuration for Google Sheets credentials and sheet details.
# - Standard csv module: For CSV file creation and writing.


import csv
from integrations import KeepaAPI, GoogleSheetsAPI
from config import settings


keepa_api = KeepaAPI()

google_sheets_api = GoogleSheetsAPI(
    credentials_file=settings.GOOGLE_SHEETS_CREDENTIALS_FILE,
    spreadsheet_id=settings.GOOGLE_SHEETS_SPREADSHEET_ID,
    range_name=settings.GOOGLE_SHEETS_RANGE_NAME
)

# Get Asins from Google Sheets
asins = google_sheets_api.get_asins_from_sheet()
asins = asins[:20]

csv_columns = [
    'ASIN',
    'Title US',
    'Title MX',
    'Brand US',
    'Brand MX',
    'Category US',
    'Category MX',
    'Description US',
    'Description MX',
    'Price US',
    'Price MX'
]
csv_data = []

# Every 5 asins is a batch to get the information from Keepa
for i in range(0, len(asins), 5):
    products_us = keepa_api.get_products_by_asins(asins[i:i + 5], domain='US')

    products_mx = keepa_api.get_products_by_asins(asins[i:i + 5], domain='MX')

    for product_us, product_mx in zip(products_us, products_mx):
        product_info_us = keepa_api.extract_product_info(product_us)
        product_info_mx = keepa_api.extract_product_info(product_mx)

        csv_data.append({
            'ASIN': product_info_us['asin'],
            'Title US': product_info_us['title'],
            'Title MX': product_info_mx['title'],
            'Brand US': product_info_us['brand'],
            'Brand MX': product_info_mx['brand'],
            'Category US': product_info_us['category'],
            'Category MX': product_info_mx['category'],
            'Description US': product_info_us['description'],
            'Description MX': product_info_mx['description'],
            'Price US': product_info_us['price'],
            'Price MX': product_info_mx['price']
        })

    print(f'Batch {i // 5 + 1} processed.')


print('Writing CSV file...')
with open('products.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    writer.writeheader()
    for data in csv_data:
        writer.writerow(data)

print('CSV file written.')

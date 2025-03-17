# Script that retrieves product information using data from both Google Sheets and the Keepa API,
# and then writes the consolidated product details to google sheets.
# Workflow:
# 1. Fetch a list of ASINs from a specified Google Sheets document.
# 2. Limit the ASIN list to the first 20 entries.
# 3. Process ASINs in batches of 5:
#     a. Retrieve product data from the Keepa API for the US domain.
#     b. Retrieve product data from the Keepa API for the MX domain.
#     c. Extract product details (ASIN, title, brand, category, description, and price) for both domains.
#     d. Combine the extracted data from US and MX into a unified format.
# 4. Write the compiled data into google sheets.
# Dependencies:
# - integrations.KeepaAPI: For interfacing with the Keepa API to obtain product data.
# - integrations.GoogleSheetsAPI: For extracting ASINs from a Google Sheets document.
# - config.settings: Provides configuration for Google Sheets credentials and sheet details.


from integrations import KeepaAPI, GoogleSheetsAPI
from config import settings

def main():
    keepa_api = KeepaAPI()

    google_sheets_api = GoogleSheetsAPI(
        credentials_file=settings.GOOGLE_SHEETS_CREDENTIALS_FILE,
        spreadsheet_id=settings.GOOGLE_SHEETS_SPREADSHEET_ID,
        range_name=settings.GOOGLE_SHEETS_RANGE_NAME
    )

    # Get Asins from Google Sheets
    asins = google_sheets_api.get_asins_from_sheet()
    asins = asins[:20]

    data = []

    # Every 5 asins is a batch to get the information from Keepa
    for i in range(0, len(asins), 5):
        products_us = keepa_api.get_products_by_asins(asins[i:i + 5], domain='US')

        products_mx = keepa_api.get_products_by_asins(asins[i:i + 5], domain='MX')

        for product_us, product_mx in zip(products_us, products_mx):
            product_info_us = keepa_api.extract_product_info(product_us)
            product_info_mx = keepa_api.extract_product_info(product_mx)
            product_info = [
                product_info_us['asin'],
                product_info_us['title'],
                product_info_us['brand'],
                product_info_us['category'],
                product_info_us['description'],
                product_info_us['price'],
                product_info_mx['price']
            ]
            data.append(product_info)

    # Write the data to Google Sheets
    google_sheets_api.update_values(data)

    print(f'Batch {i // 5 + 1} processed.')


if __name__ == '__main__':
    main()

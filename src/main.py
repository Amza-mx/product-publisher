# Description: Main entry point for the application
# Get the best sellers from Keepa and print the product information

from services import KeepaService

def main():
    keepa_service = KeepaService()
    products = keepa_service.get_best_sellers()
    
    for product in products:
        print(keepa_service.extract_product_info(product))    

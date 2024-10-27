import settings
import keepa
from services.keepa.models import ProductModel


class KeepaService:
    def __init__(self, api_key: str = settings.KEEPA_API_KEY):
        self.api = keepa.Keepa(accesskey=api_key, timeout=None)

    def get_subcategories(self, category_id: int = settings.KEEPA_CATEGORY_ID, domain: str = 'US') -> list:
        """Function to get the subcategories of a category"""

        print(f'Getting subcategories of the category {category_id}...')

        # Get the best selling products in the category
        category = self.api.category_lookup(category_id, domain=domain)
        category = category[str(category_id)]

        # Get the best 10 selling products for each subcategory
        subcategories = category['children']

        print('Subcategories retrieved.')
        print(f'Subcategories: {subcategories}')

        return subcategories

    def get_best_selling_products(self, subcategories: list, domain: str) -> list:
        """Function to get the ASINS of the best selling products of each subcategory"""

        print('Getting best selling products...')

        asins = []

        for subcategory in subcategories:
            best_sellers = self.api.best_sellers_query(subcategory, domain=domain)
            asins.extend(best_sellers)

        print('Best selling products retrieved.')
        print(f'Count of best selling products: {len(asins)}')
        print(f'ASINS: {asins}')

        return asins

    def get_best_sellers(self, category_id=settings.KEEPA_CATEGORY_ID, domain=settings.KEEPA_DOMAIN) -> list:
        """Function to get the best selling products of subcategories of a category"""

        subcategories = self.get_subcategories(category_id, domain)
        asins = self.get_best_selling_products(subcategories, domain)
        products = self.api.query(asins, domain=domain, buybox=True)

        return products

    def extract_product_info(self, product):
        """Function to extract the product information from the product details"""
        product = ProductModel(**product)
        return product.model_dump(mode='json')

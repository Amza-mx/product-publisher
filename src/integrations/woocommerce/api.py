from woocommerce import API
from config import settings


class WooCommerceAPI:
    def __init__(self):
        self.url = settings.WOOCOMMERCE_URL
        self.consumer_key = settings.WOOCOMMERCE_CONSUMER_KEY
        self.consumer_secret = settings.WOOCOMMERCE_CONSUMER_SECRET
        self.api = API(
            url=self.url,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            version="wc/v3"
        )

    def get_products(self):
        return self.api.get("products").json()

    def create_product(self, product_data: dict) -> dict:
        """Function to create a product in WooCommerce"""
        print(f'Creating product in WooCommerce: {product_data["name"]}...')
        response = self.api.post("products", data=product_data).json()
        print('Product created in WooCommerce.')
        return response

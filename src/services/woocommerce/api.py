from woocommerce import API
from settings import WOOCOMMERCE_URL, WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET

class WooCommerceAPI:
    def __init__(self):
        self.url = WOOCOMMERCE_URL
        self.consumer_key = WOOCOMMERCE_CONSUMER_KEY
        self.consumer_secret = WOOCOMMERCE_CONSUMER_SECRET
        self.api = API(
            url=self.url,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            version="wc/v3"
        )

    def get_products(self):
        return self.api.get("products").json()

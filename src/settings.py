import os
from dotenv import load_dotenv

load_dotenv()

# WooCommerce API
WOOCOMMERCE_URL = os.getenv("WOOCOMMERCE_URL", "default")
WOOCOMMERCE_CONSUMER_KEY = os.getenv("WOOCOMMERCE_CONSUMER_KEY", "default")
WOOCOMMERCE_CONSUMER_SECRET = os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "default")

# Keepa API
KEEPA_API_KEY = os.getenv("KEEPA_API_KEY", "default")
KEEPA_CATEGORY_ID = os.getenv("KEEPA_CATEGORY_ID", 0)
KEEPA_DOMAIN = os.getenv("KEEPA_DOMAIN", "US")

# OPENAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "default")
OPENAI_ENGINE_ID = os.getenv("OPENAI_ENGINE_ID", "default")

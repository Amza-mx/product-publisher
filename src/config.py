from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Google Sheets API
    GOOGLE_SHEETS_CREDENTIALS_FILE: str
    GOOGLE_SHEETS_SPREADSHEET_ID: str
    GOOGLE_SHEETS_RANGE_NAME: str

    # Keepa API
    KEEPA_API_KEY: str
    KEEPA_DOMAIN: str

    # OPENAI API
    OPENAI_API_KEY: str
    OPENAI_ENGINE_ID: str

    # WooCommerce API
    WOOCOMMERCE_URL: str
    WOOCOMMERCE_CONSUMER_KEY: str
    WOOCOMMERCE_CONSUMER_SECRET: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

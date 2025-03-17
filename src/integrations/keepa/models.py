from typing import List, Optional
from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    title: Optional[str] = Field(None, description="Título del producto")
    asin: Optional[str] = Field(None, description="ASIN del producto")
    price: Optional[float] = Field(None, description="Precio del producto en USD")
    brand: Optional[str] = Field(None, description="Marca del producto")
    description: Optional[str] = Field(None, description="Descripción del producto")
    features: Optional[List[str]] = Field(default_factory=list, description="Características del producto")
    categories: Optional[List[int]] = Field(default_factory=list, description="Categorías del producto")
    images: Optional[List[str]] = Field(default_factory=list, description="URLs de las imágenes del producto")


    def get_buy_box_price(self, values: dict) -> float:
        """Function to get the last buy box price of the product"""
        data = values.get('data')
        if data:
            # Get the last buybox price of the product
            buybox_prices = data.get('BUY_BOX_SHIPPING', [])
            if len(buybox_prices) > 0:
                # cast np.float64 to float
                return float(buybox_prices[-1])  # Keepa prices are in cents
        return 0

    def get_category_label(self, value) -> str:
        """Function to get the label of a category"""
        category_tree = value['categoryTree'] if value.get('categoryTree') else []
        root_category = value['rootCategory'] if value.get('rootCategory') else ''
        for category in category_tree:
            if category['catId'] == root_category:
                return category['name']
        return ''
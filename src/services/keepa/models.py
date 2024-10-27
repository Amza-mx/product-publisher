from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class ProductModel(BaseModel):
    title: str
    price: Optional[float] = Field(None, description="Precio del producto en USD")
    description: Optional[str] = Field(None, description="Descripción del producto")
    # in_stock: bool = Field(..., description="Disponibilidad del producto en stock")
    features: List[str] = Field(default_factory=list, description="Características del producto")

    @field_validator('price', mode='before')
    def validate_price(cls, v, values):
        data = values.get('data')
        if data:
            # Get the last NEW price of the product
            price = data.get('NEW', [None])[-1] if data.get('NEW') else 0
            return price
        return v

from typing import List, Optional
from pydantic import BaseModel, Field
from src.schemas.client import ClientSchema
from src.schemas.product import CartProductSchema



class ShopcartSchema(BaseModel):
    client: ClientSchema
    products: List[CartProductSchema]
    is_open: bool = Field(default=True)
    quantity_cart: Optional[int]
    value: Optional[float] = Field(default=0.0)


class UpdateShopcartSchema(BaseModel):
    quantity_product: Optional[int] = Field(default=0)

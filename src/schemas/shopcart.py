from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from src.schemas.client import ClientSchema
from src.schemas.product import ProductSchema



class ShopcartSchema(BaseModel):
    client: ClientSchema
    products: List[ProductSchema]
    is_open: bool = Field(default=True)
    quantity_cart: int
    value: Optional[float] = Field(default=0.0)


class NewshopcartSchema(BaseModel):
    is_open: Optional[bool] = Field(default=True)
    quantity_cart: Optional[int] = Field(default=0)
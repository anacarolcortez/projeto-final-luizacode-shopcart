from typing import List
from pydantic import BaseModel

from src.schemas.order import OrderSchema
from src.schemas.product import ProductSchema


class OrderItemsSchema(BaseModel):
    order: OrderSchema
    products: ProductSchema
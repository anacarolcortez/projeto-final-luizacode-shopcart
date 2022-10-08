from enum import unique
from pydantic import BaseModel, Field
from bson import ObjectId
from src.schemas.product import ProductSchema


class StockSchema(BaseModel):
    product: ProductSchema 
    stock_quantity: int


class StockQuantitySchema(BaseModel):
    stock_quantity: int
 
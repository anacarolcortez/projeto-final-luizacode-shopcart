from fastapi import APIRouter
from src.models.stock import create_product_stock
from src.schemas.stock import StockQuantitySchema
from src.server.database import db


router = APIRouter(prefix="/stocks")


@router.post("/{code}", tags=["stocks"])
async def post_product_stock(code: str, stock: StockQuantitySchema):
    return await create_product_stock(
        code,
        stock
    )

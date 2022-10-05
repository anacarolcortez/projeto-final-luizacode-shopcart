from fastapi import APIRouter
from src.models.shopcart import create_shopcart
from src.schemas.shopcart import NewshopcartSchema, ShopcartSchema
from src.server.database import db



router = APIRouter(prefix="/shopcarts")
shopcarts_collection = db.shopcarts_collection
clients_collection = db.clients_collection
products_collection = db.products_collection

@router.post("/", tags=["shopcarts"])
async def post_shopcart(shopcart:NewshopcartSchema, email: str, code:str):
    return await create_shopcart(
        shopcarts_collection,
        clients_collection,
        products_collection,
        shopcart,
        email,
        code
    )
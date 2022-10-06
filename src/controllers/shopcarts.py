from fastapi import APIRouter
from src.models.shopcart import create_shopcart
from src.schemas.shopcart import NewShopcartSchema
from src.server.database import db



router = APIRouter(prefix="/shopcarts")
shopcarts_collection = db.shopcarts_collection
clients_collection = db.clients_collection
products_collection = db.products_collection

@router.post("/{email}/{code}", tags=["shopcarts"])
async def post_shopcart(email: str, code:str, new_cart: NewShopcartSchema):
    return await create_shopcart(
        shopcarts_collection,
        clients_collection,
        products_collection,
        email,
        code,
        new_cart
    )
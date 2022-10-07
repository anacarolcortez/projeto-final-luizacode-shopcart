from fastapi import APIRouter
from src.models.shopcart import create_shopcart, update_cart
from src.schemas.shopcart import NewShopcartSchema, UpdateShopcartSchema
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
    
    
@router.patch("/{email}/{code}", tags=["shopcarts"])
async def patch_shopcart(email: str, code:str, product_quantity: UpdateShopcartSchema):
    return await update_cart(
        shopcarts_collection,
        clients_collection,
        products_collection,
        email,
        code,
        product_quantity
    )
    
#delete: excluir produto do carrinho e fazer update da quantidade, se carrinho zerado excluir ele também

#get carrinho aberto
#get carriho fechado
#put: fechar carrinho aberto (update de propriedade is_openned)
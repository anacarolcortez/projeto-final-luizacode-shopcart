from fastapi import APIRouter
from src.models.shopcart import create_shopcart, get_closed_cart, get_opened_cart, put_closed_shopcart, update_cart
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

@router.get("/opened/{email}/", tags=["shopcarts"])
async def get_shopcart_open(email: str):
    return await get_opened_cart(
        shopcarts_collection,
        email
    )

@router.get("/closed/{email}/", tags=["shopcarts"])
async def get_shopcart_close(email: str, skip = 0, limit = 10):
    return await get_closed_cart(
        shopcarts_collection,
        email,
        skip,
        limit
    )  

@router.put("/close/{email}/", tags=["shopcarts"])
async def closing_shopcart(email: str):
    return await put_closed_shopcart(
        shopcarts_collection,
        email
    )  

#delete: excluir produto do carrinho e fazer update da quantidade, se carrinho zerado excluir ele também

#get carrinho aberto
#get carriho fechado
#put: fechar carrinho aberto (update de propriedade is_openned)
from fastapi import APIRouter, Depends
from src.models.shopcart import (
    create_shopcart, get_closed_cart, 
    get_opened_cart, put_closed_shopcart, update_cart, update_cart_delete_item
)
from src.schemas.shopcart import UpdateShopcartSchema
from src.security.basic_auth import validate_credentials
from src.server.database import db


router = APIRouter(prefix="/shopcarts")


@router.post("/{email}/{code}", tags=["shopcarts"])
async def post_shopcart(code: str, product_quantity: UpdateShopcartSchema, email: str=Depends(validate_credentials)):
    try:
        return await create_shopcart(
            email,
            code,
            product_quantity
        )
    except Exception as e:
        return f'{e}'


@router.patch("/{email}/{code}", tags=["shopcarts"])
async def patch_shopcart(code: str, product_quantity: UpdateShopcartSchema, email: str=Depends(validate_credentials)):
    try:
        return await update_cart(
            email,
            code,
            product_quantity
        )
    except Exception as e:
        return f'{e}'


@router.get("/opened/{email}/", tags=["shopcarts"])
async def get_shopcart_open(email: str=Depends(validate_credentials)):
    try:
        return await get_opened_cart(
            email
        )
    except Exception as e:
        return f'{e}'


@router.get("/closed/{email}/", tags=["shopcarts"])
async def get_shopcart_close(skip=0, limit=10, email: str=Depends(validate_credentials)):
    try:
        return await get_closed_cart(
            email,
            skip,
            limit
        )
    except Exception as e:
        return f'{e}'


@router.put("/close/{email}/", tags=["shopcarts"])
async def closing_shopcart(email: str=Depends(validate_credentials)):
    try:
        return await put_closed_shopcart(
            email
        )
    except Exception as e:
        return f'{e}'


@router.delete("/{email}/{code}", tags=["shopcarts"])
async def remove_item_quantity_from_cart(code: str, product_quantity: UpdateShopcartSchema, 
                                email: str=Depends(validate_credentials)):
    try:
        return await update_cart_delete_item(
            email, 
            code, 
            product_quantity
        )
    except Exception as e:
        return f'{e}'

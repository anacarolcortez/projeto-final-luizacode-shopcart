from src.models.product import (
    create_product,
    get_product,
    update_product,
    delete_product,
    get_products
)
from fastapi import APIRouter
from src.schemas.product import ProductSchema, UserName
from src.server.database import db

router = APIRouter(prefix="/products")
products_collection = db.products_collection


@router.post("/", tags=["products"])
async def post_product(product: ProductSchema):
    return await create_product(
        products_collection,
        product
    )

@router.get("/{code}", tags=["products"])
async def get_product_by_code(code: str):
    return await get_product(
        products_collection,
        code
    )

@router.get("/{name}", tags=["products"])
async def get_product_by_name(name: str):
    return await get_product(
        products_collection,
        name
    )

@router.patch("/{code}", tags=["products"])
async def patch_product_email(code: str, name: UserName):
    is_updated, numbers_updated = await update_product(
        products_collection,
        code,
        name
    )
    if is_updated:
        return f"Atualização realizada com sucesso, número de documentos alterados {numbers_updated}"
    else:
        return "Atualização falhou!"


@router.delete("/{code}", tags=["products"])
async def delete_product_by_id(code: str):
    return await delete_product(
        products_collection,
        code
    )


@router.get("/", tags=["products"])
async def get_all_products():
    return await get_products(
        products_collection,
        skip=0,
        limit=10
    )

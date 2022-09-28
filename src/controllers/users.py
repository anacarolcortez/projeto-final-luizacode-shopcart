from src.models.user import (
    create_user,
    get_user,
    update_user,
    delete_user,
    get_users
)
from fastapi import APIRouter
from src.schemas.user import UserSchema, UserPassword
from src.server.database import db

router = APIRouter(prefix="/usuarios")
users_collection = db.users_collection


@router.post("/")
async def post_user(user: UserSchema):
    return await create_user(
        users_collection,
        user
    )


@router.get("/{id}")
async def get_user_by_id(id: str):
    return await get_user(
        users_collection,
        id
    )


@router.patch("/{id}")
async def patch_user_email(id: str, password: UserPassword):
    is_updated, numbers_updated = await update_user(
        users_collection,
        id,
        password
    )
    if is_updated:
        return f"Atualização realizada com sucesso, número de documentos alterados {numbers_updated}"
    else:
        return "Atualização falhou!"


@router.delete("/{id}")
async def delete_user_by_id(id: str):
    return await delete_user(
        users_collection,
        id
    )


@router.get("/")
async def get_all_users():
    return await get_users(
        users_collection,
        skip=0,
        limit=10
    )

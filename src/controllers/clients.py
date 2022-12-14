from src.models.clients import (
    create_client,
    get_all_clients,
    get_client_by_email,
)
from fastapi import APIRouter, Depends
from src.schemas.client import UserClientSchema
from src.security.basic_auth import validate_credentials
from src.server.database import db

router = APIRouter(prefix="/clients")


@router.post("/", tags=["clients"])
async def post_client(client: UserClientSchema):
    return await create_client(
        client
    )


@router.get("/{email}", tags=["clients"])
async def get_client(email: str=Depends(validate_credentials)):
    try:
        return await get_client_by_email(
            email
        )
    except Exception as e:
        return f'{e}'


@router.get("/", tags=["clients"])
async def list_clients():
    return await get_all_clients(
        skip=0,
        limit=10
    )
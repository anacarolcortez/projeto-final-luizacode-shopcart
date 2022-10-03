from src.models.clients import (
    create_client,
    get_client_by_email,
)
from fastapi import APIRouter
from src.schemas.client import ClientSchema
from src.server.database import db

router = APIRouter(prefix="/clients")
clients_collection = db.clients_collection


@router.post("/", tags=["clients"])
async def post_client(client: ClientSchema):
    return await create_client(
        clients_collection,
        client
    )


@router.get("/{email}", tags=["clients"])
async def get_client(email: str):
    return await get_client_by_email(
        clients_collection,
        email
    )

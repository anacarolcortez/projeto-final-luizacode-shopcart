from src.models.address import (
    create_address,
    get_address_by_zipcode,
    get_addresses
)
from fastapi import APIRouter
from src.schemas.address import AddressSchema
from src.server.database import db

router = APIRouter(prefix="/address")
address_collection = db.address_collection


@router.post("/", tags=["address"])
async def post_address(address: AddressSchema):
    return await create_address(
        address_collection,
        address
    )


@router.get("/{zipcode}", tags=["address"])
async def get_address(zipcode: str):
    return await get_address_by_zipcode(
        address_collection,
        zipcode
    )


@router.get("/", tags=["address"])
async def get_all_address():
    return await get_addresses(
        address_collection,
        skip=0,
        limit=10
    )

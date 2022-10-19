from src.models.address import (
    create_address,
    get_address_by_zipcode,
    get_addresses
)
from fastapi import APIRouter
from src.schemas.address import AddressSchema
from src.server.database import db

router = APIRouter(prefix="/address")


@router.post("/", tags=["address"])
async def post_address(address: AddressSchema):
    return await create_address(
        address
    )


@router.get("/{zipcode}", tags=["address"])
async def get_address(zipcode: str):
    return await get_address_by_zipcode(
        zipcode
    )


@router.get("/", tags=["address"])
async def get_all_address():
    return await get_addresses(
        skip=0,
        limit=10
    )

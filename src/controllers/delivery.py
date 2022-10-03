from src.models.delivery import (
    create_user_delivery_address,
    get_delivery_address_by_email,
    delete_delivery_address_by_zipcode
)
from fastapi import APIRouter
from src.schemas.delivery import DeliverySchema
from src.schemas.address import AdressComplementSchema
from src.server.database import db

router = APIRouter(prefix="/deliveryaddress")
delivery_collection = db.delivery_collection
clients_collection = db.clients_collection
address_collection = db.address_collection


@router.post("/{email}/{zipcode}", tags=["delivery"])
async def post_delivery_address(email: str, zipcode:str, address: AdressComplementSchema):
    return await create_user_delivery_address(
        delivery_collection,
        clients_collection,
        address_collection,
        email,
        zipcode,
        address
    )


@router.get("/{email}", tags=["delivery"])
async def get_delivery_address(email: str):
    return await get_delivery_address_by_email(
        delivery_collection,
        email
    )


@router.delete("/{zipcode}/client/{email}", tags=["delivery"])
async def delete_delivery_address(zipcode: str, email: str):
    return await delete_delivery_address_by_zipcode(
        delivery_collection,
        zipcode,
        email
    )

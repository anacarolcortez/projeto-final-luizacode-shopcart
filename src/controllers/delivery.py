from src.models.delivery import (
    create_user_delivery_address,
    get_delivery_address_by_email
)
from fastapi import APIRouter, Depends
from src.schemas.address import AdressComplementSchema
from src.security.basic_auth import validate_credentials
from src.server.database import db

router = APIRouter(prefix="/deliveryaddress")


@router.post("/{email}/{zipcode}", tags=["delivery"])
async def post_delivery_address(zipcode:str, address: AdressComplementSchema, email: str=Depends(validate_credentials)):
    try:
        return await create_user_delivery_address(
            email,
            zipcode,
            address
        )
    except Exception as e:
        return f'{e}'


@router.get("/{email}", tags=["delivery"])
async def get_delivery_address(email: str=Depends(validate_credentials)):
    try:
        return await get_delivery_address_by_email(
            email
        )
    except Exception as e:
        return f'{e}'
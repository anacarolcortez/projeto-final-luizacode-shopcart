import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

from src.schemas.address import Address
from src.schemas.user import UserSchema

class Order(BaseModel):
    user: UserSchema
    price: Decimal
    paid: bool
    create: datetime.datetime
    address: Address
    authority: Optional[str]

class OrderSchema(BaseModel):
    price: Optional[Decimal] = Field(max_digits=10, decimal_places=2, default=0.0)
    paid: bool = Field(default=False)
    create: datetime.datetime = Field(default=datetime.datetime.now())
    authority: Optional[str] = Field(max_length=100)

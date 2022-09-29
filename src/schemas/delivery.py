from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from src.schemas.address import AddressSchema
from src.schemas.client import ClientSchema


class DeliverySchema(BaseModel):
    client: ClientSchema
    address: List[AddressSchema]
    
    class Config:
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                    "delivery" : [
                        {
                            "street_number": 123,
                            "complement": "2nd floor",
                            "is_delivery": True
                        }
                    ]
            }
        }

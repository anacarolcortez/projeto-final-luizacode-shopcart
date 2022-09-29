from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class AddressSchema(BaseModel):
    zipcode: str = Field(max_length=8, unique=True, index=True)
    street: str = Field(max_length=100)
    city: str = Field(max_length=20)
    state: str = Field(max_length=20)
    
    class Config:
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                    "address" : [
                        {
                            "zipcode": "01021030",
                            "street": "Tree Fort",
                            "city": "City of Grass",
                            "state": "Land of Ooo"
                        }
                    ]
            }
        }
        
class AdressComplement(BaseModel):
    street_number: int = Field(max_length=6)
    complement: Optional[str] = Field(max_length=20)
    is_delivery: bool = Field(default=True)

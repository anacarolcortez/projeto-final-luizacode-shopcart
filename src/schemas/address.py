from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId


from src.schemas.user import UserSchema


class Address(BaseModel):
    street: str
    zipcode: str
    district: str
    city: str
    state: str
    is_delivery: bool = Field(default=True)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                    "address" : [
                        {
                            "street": "Tree Fort",
                            "zipcode": "01020-030",
                            "district": "Grass Lands",
                            "city": "Land of Ooo",
                            "state": "Parallel Universe", 
                            "is_delivery": True
                        }
                    ]
            }
        }



class AddressSchema(BaseModel):
    user: UserSchema
    address: List[Address] = []
    

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                  "user": {
                        "name": "Finn The Human",
                        "email": "herofinn@adventuretime.com",
                        "password": "dieLich!",
                        "is_active": True,
                        "is_admin": False
                    },
                    "address" : [
                        {
                            "street": "Tree Fort",
                            "zipcode": "01020-030",
                            "district": "Grass Lands",
                            "city": "Land of Ooo",
                            "state": "Parallel Universe", 
                            "is_delivery": True
                        },
                        {
                            "street": "Candy Castle",
                            "zipcode": "01020-040",
                            "district": "Candy Kingdom",
                            "city": "Land of Ooo",
                            "state": "Parallel Universe", 
                            "is_delivery": False
                        }
                    ]
            }
        }

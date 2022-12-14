from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from bson import ObjectId


class ClientSchema(BaseModel):
    name: str = Field(max_length=100)
    email: EmailStr = Field(unique=True, index=True)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Daenerys Targaryen",
                "email": "khaleesi@dracarys.com"
            }
        }


class UserClientSchema(BaseModel):
    name: str = Field(max_length=100)
    email: EmailStr = Field(unique=True, index=True)
    password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Daenerys Targaryen",
                "email": "khaleesi@dracarys.com",
                "password": "motherOfDragons3"
            }
        }

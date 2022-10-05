from typing import Optional
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from bson import ObjectId


class ClientSchema(BaseModel):
    name: str = Field(max_length=100)
    email: EmailStr = Field(unique=True, index=True)
    cpf: str = Field(min_length=11, max_length=11, unique=True)
    user_id: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Daenerys Targaryen", 
                "email": "khaleesi@dracarys.com",
                "cpf": "12345678910"
            }
        }

class UserPassword(BaseModel):
    password: str

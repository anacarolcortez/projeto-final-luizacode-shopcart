from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from bson import ObjectId


class UserSchema(BaseModel):
    email: EmailStr = Field(unique=True, index=True)
    password: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "khaleesi@dracarys.com",
                "password": "motherOfDragons3",
                "is_active": True,
                "is_admin": False
            }
        }

class UserPassword(BaseModel):
    password: str

from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from bson import ObjectId


class UserSchema(BaseModel):
    name: str = Field(max_length=80)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Daenerys Targaryen",
                "email": "khaleesi@dracarys.com",
                "password": "motherOfDragons3",
                "is_active": True,
                "is_admin": False
            }
        }

# Teste de update de email (precisa passar Schema como parâmetro na api para ser reconhecido como body da requisição)


class UserPassword(BaseModel):
    password: str

from pydantic import BaseModel, Field
from bson import ObjectId


class ProductSchema(BaseModel):
    name: str = Field(max_length=100)
    description: str
    price: float
    image: str
    code: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Iron Throne",
                "description": "forged at the order of Aegon the Conqueror, the first of the Targaryen Kings, who conquered six of the seven independent kingdoms of Westeros; made of 1.000 swords",
                "price": 5690.9,
                "image": "http://127.0.0.1:8000/produto/ironthrone.png",
                "code": 123456789
            }
        }

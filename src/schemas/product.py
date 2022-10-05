from enum import unique
from pydantic import BaseModel, Field
from bson import ObjectId

class AttributesSchema(BaseModel):
    RAM_memory: str
    technology: str
    connectivity: str
    processor: str
    operational_system: str

class ProductSchema(BaseModel):
    name: str = Field(max_length=100)
    description: str
    price: float
    quantity: int
    image: str
    code: str = Field(unique=True)
    attributes: AttributesSchema

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Smartphone Motorola Moto E7 32GB Cinza",
                "description": "O smartphone Moto E7 é perfeito para te ajudar nas tarefas básicas do dia a dia, como utilizar aplicativos de mensagens, ligações e envio de SMS. Possui um design elegante, sofisticado e moderno. Sua câmera frontal tem a resolução de 5MP, já as traseiras possuem 48MP e 2MP de resolução. A tela de 6,5 polegadas IPS Max Vision conta com resolução HD+ para garantir uma ótima visualização ao assistir seus conteúdos favoritos, como filmes e séries. Com 32GB de armazenamento interno, ele é ideal para guardar suas fotos, músicas ou vídeos! E se mesmo assim achar pouco, você pode usar um cartão MicroSD de até 512GB para aumentar essa capacidade. Possui o processador MediaTek Helio G2 Octa-Core juntamente com sua memória RAM de 2GB. Fique sempre conectado com a tecnologia 4G em um aparelho dual chip e tenha bateria para navegar o dia todo com 4000mAh. O leitor de impressão digital garante que os seus conteúdos e dados fiquem sempre super protegidos.",
                "price": 809.10,
                "value_estoque": 10,
                "image": "http://127.0.0.1:8000/produto/Smartphone.png",
                "code": 123456789,
                "atributo": {
                    "RAM memory": "2G",
                    "technology": "4G",
                    "connectivity": "Bluetooth - Wi-Fi",
                    "processor": "Octa-Core",
                    "operational system": "Android"  
                }
            }
        }
        
class UserName(BaseModel):
    name: str

    
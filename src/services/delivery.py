from fastapi.encoders import jsonable_encoder
from bson import json_util
import json

from server.database import db
delivery_collection = db.delivery_collection

async def get_user_delivery_address(email):
    delivery_address = await delivery_collection.find_one({'client.email': email})
    if delivery_address:
        return json.loads(json_util.dumps(delivery_address))
    else:
        return None
    

async def create_delivery_data(client, address, add_compl):
    address_payload = {
        "address": address,
        "complement": jsonable_encoder(add_compl)
    }

    delivery = await delivery_collection.insert_one(
        {
            "client": client,
            "address": [address_payload]
        }
    )
    if delivery.inserted_id:
        return await get_user_delivery_address(client['email'])
    else:
        raise Exception("Erro ao associar endereço para este usuário")


async def upsert_client_address(email, address, add_compl):
    address_payload = {
        "address": address,
        "complement": jsonable_encoder(add_compl)
    }

    data = await delivery_collection.update_one(
        {"client.email": email},
        {
            "$addToSet": {
                "address": address_payload
            }
        }
    )
    if data.modified_count:
        response = await get_user_delivery_address(email)
        return json.loads(json_util.dumps(response))
    else:
        raise Exception("Usuário já possui este endereço cadastrado")
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json


async def create_client(clients_collection, client):
    try:
        already_exists = await get_client_by_email(clients_collection, client.email)
        if already_exists:
            raise Exception(
                "Um usuário com este e-mail já está cadastrado no sistema")
        else:
            valid_email = await validate_email(client.email)
            if valid_email:
                data = await clients_collection.insert_one(jsonable_encoder(client))
                if data.inserted_id:
                    return await get_client_by_id(clients_collection, data.inserted_id)
                else:
                    raise Exception("Erro ao cadastrar cliente")
            else:
                raise Exception(
                    "Texto que antecede o @ precisa ter acima de 3 caracteres")
    except Exception as e:
        return f'create_client.error: {e}'


async def get_client_by_id(clients_collection, client_id):
    try:
        client = await clients_collection.find_one({'_id': ObjectId(client_id)})
        if client:
            return json.loads(json_util.dumps(client))
    except Exception as e:
        return f'get_client_by_id.error: {e}'


async def get_client_by_email(clients_collection, email):
    try:
        client = await clients_collection.find_one({'email': email})
        if client:
            return json.loads(json_util.dumps(client))
    except Exception as e:
        return f'get_client_by_email.error: {e}'


async def validate_email(email):
    # the attribute is set as "Emailstr" in Clients Schema, which validates email syntax
    user_email = email.split("@")[0]
    if len(user_email) >= 3:
        return True
    return False

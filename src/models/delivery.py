from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json

from src.models.address import get_address_by_zipcode
from src.models.clients import get_client_by_email


async def create_user_delivery_address(delivery_collection, clients_collection,
                                       address_collection, email, zipcode, add_compl):
    try:
        client, address = await get_user_and_address(
            clients_collection, address_collection, email, zipcode)
        if client and address:
            user_has_delivery_data = await get_user_delivery_address(delivery_collection, email)
            if user_has_delivery_data:
                return await upsert_client_address(delivery_collection, email, address, add_compl)
            else:
                return await create_delivery_data(delivery_collection, client, address, add_compl)
        else:
            raise Exception(
                "Informe e-mail e cep existentes para o cadastro de endereços do usuário")
    except Exception as e:
        return f'create_user_delivery_address.error: {e}'


async def get_delivery_address_by_email(delivery_collection, email):
    try:
        delivery = await delivery_collection.find_one({'client.email': email})
        if delivery:
            return json.loads(json_util.dumps(delivery))
        else:
            raise Exception("Não há endereços associados ao e-mail informado")
    except Exception as e:
        return f'get_delivery_address_by_email.error: {e}'


async def delete_delivery_address_by_zipcode(zipcode, email):
    pass


async def get_user_and_address(clients_collection, address_collection, email, zipcode):
    client = await get_client_by_email(clients_collection, email)
    address = await get_address_by_zipcode(address_collection, zipcode)
    return client, address


async def get_user_delivery_address(delivery_collection, email):
    try:
        delivery_address = await delivery_collection.find_one({'client.email': email})
        if delivery_address:
            return json.loads(json_util.dumps(delivery_address))
    except Exception as e:
        return f'get_user_delivery_address.error: {e}'


async def create_delivery_data(delivery_collection, client, address, add_compl):
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
        return await get_delivery_address_by_email(delivery_collection, client['email'])

    raise Exception("Erro ao criar lista de endereços para usuário")


async def upsert_client_address(delivery_collection, email, address, add_compl):
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
        response = await get_delivery_address_by_email(delivery_collection, email)
        return json.loads(json_util.dumps(response))

    raise Exception("Endereço já existe na lista deste usuário")

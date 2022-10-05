from fastapi.encoders import jsonable_encoder
from src.services.clients import (find_one_client_by_email, get_clients_list, 
                                  insert_one_new_client)


async def create_client(clients_collection, client):
    try:
        client_data = await find_one_client_by_email(clients_collection, client.email)
        if client_data is not None:
            raise Exception(
                "Um usuário com este e-mail já está cadastrado no sistema")

        valid_email = await validate_email(client.email)
        if not valid_email:
            raise Exception("Usuário do email deve ter mais de 3 caracteres")
        
        return await insert_one_new_client(clients_collection, jsonable_encoder(client))
            
    except Exception as e:
        return f'create_client.error: {e}'


async def get_client_by_email(clients_collection, email):
    try:
        client = await find_one_client_by_email(clients_collection, email)
        if client is not None:
            return client
        else:
            raise Exception("Cliente não encontrado no sistema")
    except Exception as e:
        return f'get_client_by_email.error: {e}'


async def validate_email(email):
    user_email = email.split("@")[0]
    if len(user_email) >= 3:
        return True
    return False


async def get_all_clients(clients_collection, skip, limit):
    try:
        return await get_clients_list(clients_collection, skip, limit)
    except Exception as e:
        return f'get_addresses.error: {e}'
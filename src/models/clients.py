from fastapi.encoders import jsonable_encoder
from src.models.user import insert_one_user
from src.schemas.client import ClientSchema
from src.schemas.user import UserSchema
from src.services.clients import (find_one_client_by_email, get_clients_list, 
                                  insert_one_new_client)


async def create_client(clients_collection, users_collection, client):
    try:
        client_data = await find_one_client_by_email(clients_collection, client.email)
        if client_data is not None:
            raise Exception(
                "Um usuário com este e-mail já está cadastrado no sistema")

        valid_email = await validate_email(client.email)
        if not valid_email:
            raise Exception("Usuário do email deve ter mais de 3 caracteres")
        
        
        create_client = ClientSchema(
            name=client.name, 
            email=client.email
        )
        
        create_user = UserSchema(
            email=client.email,
            password=client.password
        )
        
        user_client = await insert_one_user(users_collection, create_user)
        if user_client:
            return await insert_one_new_client(clients_collection, jsonable_encoder(create_client))
        raise Exception("Erro ao cadastrar cliente no sistema")
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
from fastapi.encoders import jsonable_encoder
from src.services.user import insert_one_user
from src.schemas.client import ClientSchema
from src.schemas.user import UserSchema
from src.services.clients import (find_one_client_by_email, get_clients_list, 
                                  insert_one_new_client)


async def create_client(client):
    try:
        client_data = await find_one_client_by_email(client.email)
        if client_data is not None:
            raise Exception(
                "Um usuário com este e-mail já está cadastrado no sistema")        
        
        create_client = ClientSchema(
            name=client.name, 
            email=client.email
        )
        
        create_user = UserSchema(
            email=client.email,
            password=client.password
        )
        
        user_client = await insert_one_user(create_user)
        if user_client:
            return await insert_one_new_client(jsonable_encoder(create_client))
        raise Exception("Erro ao cadastrar cliente no sistema")
    except Exception as e:
        return f'create_client.error: {e}'


async def get_client_by_email(email):
    try:
        client = await find_one_client_by_email(email)
        if client is not None:
            return client
        else:
            raise Exception("Cliente não encontrado no sistema")
    except Exception as e:
        return f'get_client_by_email.error: {e}'


async def get_all_clients(skip, limit):
    try:
        return await get_clients_list(skip, limit)
    except Exception as e:
        return f'get_addresses.error: {e}'
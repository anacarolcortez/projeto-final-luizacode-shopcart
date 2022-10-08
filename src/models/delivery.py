from src.models.address import get_address_by_zipcode
from src.models.clients import get_client_by_email
from src.services.delivery import (create_delivery_data, 
                                   get_user_delivery_address, 
                                   upsert_client_address)


async def get_user_and_address(clients_collection, address_collection, email, zipcode):
    client = await get_client_by_email(clients_collection, email)
    address = await get_address_by_zipcode(address_collection, zipcode)
    return client, address


async def create_user_delivery_address(delivery_collection, clients_collection,
                                       address_collection, email, zipcode, add_compl):
    try:
        client, address = await get_user_and_address(
            clients_collection, address_collection, email, zipcode)
        if type(client) == dict and type(address) == dict:
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
        delivery = await get_user_delivery_address(delivery_collection, email)
        if delivery:
            return delivery
        else:
            raise Exception("Não há endereços associados ao e-mail informado")
    except Exception as e:
        return f'get_delivery_address_by_email.error: {e}'

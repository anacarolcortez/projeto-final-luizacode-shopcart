from fastapi.encoders import jsonable_encoder
from bson import json_util
import json

from src.services.address import (
    create_one_address, 
    find_address_by_zipcode, 
    get_addresses_list
)

async def create_address(address):
    try:
        already_exists = await find_address_by_zipcode(address.zipcode)
        if already_exists is not None:
            raise Exception("Um endereço com este cep já está cadastrado no sistema")
        else:
            return await create_one_address(jsonable_encoder(address))
    except Exception as e:
        return f'create_address.error: {e}'   
    

async def get_address_by_zipcode(zipcode):
    try:
        data = await find_address_by_zipcode(zipcode)
        if data is not None:
            return json.loads(json_util.dumps(data))
        else:
            raise Exception("Endereço não encontrado")
    except Exception as e:
        return f'get_address_by_zipcode.error: {e}'   

       
async def get_addresses(skip, limit):
    try:
        return await get_addresses_list(skip, limit)
    except Exception as e:
        return f'get_addresses.error: {e}'

from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json

async def create_address(address_collection, address):
    try:
        already_exists = await get_address_by_zipcode(address_collection, address.zipcode)
        if already_exists:
            raise Exception("Um endereço com este cep já está cadastrado no sistema")
        else:
            data = await address_collection.insert_one(jsonable_encoder(address))
            if data.inserted_id:
                return await get_address_by_id(address_collection, data.inserted_id)
    except Exception as e:
        return f'create_address.error: {e}'


async def get_address_by_id(address_collection, address_id):
    try:
        address = await address_collection.find_one({'_id': ObjectId(address_id)})
        if address:
            return json.loads(json_util.dumps(address))
    except Exception as e:
        return f'get_address_by_id.error: {e}'     
    

async def get_address_by_zipcode(address_collection, zipcode):
    try:
        data = await address_collection.find_one({'zipcode': zipcode})
        if data:
            return json.loads(json_util.dumps(data))
    except Exception as e:
        return f'get_address_by_zipcode.error: {e}'   

       
async def get_addresses(address_collection, skip, limit):
    try:
        address_cursor = address_collection.find().skip(int(skip)).limit(int(limit))
        address = await address_cursor.to_list(length=int(limit))
        return json.loads(json_util.dumps(address))
    except Exception as e:
        return f'get_addresses.error: {e}'

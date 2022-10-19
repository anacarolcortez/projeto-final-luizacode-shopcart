from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json

from server.database import db
address_collection = db.address_collection

async def create_one_address(address):
    data = await address_collection.insert_one(address)
    if data.inserted_id:
        return await get_address_by_id(data.inserted_id)
    raise Exception("Erro ao cadastrar endereço")


async def get_address_by_id(address_id):
    address = await address_collection.find_one({'_id': ObjectId(address_id)})
    if address is not None:
        return json.loads(json_util.dumps(address))
    else:
        return None


async def find_address_by_zipcode(zipcode):
    address = await address_collection.find_one({'zipcode': zipcode})
    if address is not None:
        return json.loads(json_util.dumps(address))
    else:
        return None

async def get_addresses_list(skip, limit):
    address_cursor = address_collection.find().skip(int(skip)).limit(int(limit))
    if address_cursor:
        address = await address_cursor.to_list(length=int(limit))
        return json.loads(json_util.dumps(address))
    raise Exception("Não há endereços cadastrados")
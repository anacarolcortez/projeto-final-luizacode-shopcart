from bson import ObjectId
from bson import json_util
import json


async def find_one_client_by_email(clients_collection, email):
    client = await clients_collection.find_one({'email': email})
    if client is not None:
        return json.loads(json_util.dumps(client))
    else:
        return None
    

async def find_one_client_by_id(clients_collection, client_id):
    client = await clients_collection.find_one({'_id': ObjectId(client_id)})
    if client is not None:
        return json.loads(json_util.dumps(client))
    else:
        return None
    
    
async def insert_one_new_client(clients_collection, client):
    data = await clients_collection.insert_one(client)
    if data.inserted_id:
        return await find_one_client_by_id(clients_collection, data.inserted_id)
    raise Exception("Erro ao cadastrar novo cliente")


async def get_clients_list(clients_collection, skip, limit):
    clients_cursor = clients_collection.find().skip(int(skip)).limit(int(limit))
    if clients_cursor:
        clients = await clients_cursor.to_list(length=int(limit))
        return json.loads(json_util.dumps(clients))
    raise Exception("Não há endereços cadastrados")
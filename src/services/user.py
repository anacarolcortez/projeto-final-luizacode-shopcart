from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json

from server.database import db
users_collection = db.users_collection

async def insert_one_user(user):
    already_exists = await get_user_by_email(user.email)
    if already_exists:
        raise Exception("Usuário já cadastrado no sistema")
    else:
        data = await users_collection.insert_one(jsonable_encoder(user))
        if data.inserted_id:
            return True
    return False


async def get_user(user_id):
    try:
        user = await users_collection.find_one({'_id': ObjectId(user_id)})
        if user:
            return json.loads(json_util.dumps(user))
    except Exception as e:
        return f'get_user.error: {e}'
        

async def get_user_by_email(email):
    try:
        user = await users_collection.find_one({'email': email})
        if user:
            return json.loads(json_util.dumps(user))
    except Exception as e:
        return f'get_user.error: {e}'
        

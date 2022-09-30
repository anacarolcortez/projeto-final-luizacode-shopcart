from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json

async def create_user(users_collection, user):
    try:
        already_exists = await get_user_by_email(users_collection, user.email)
        if already_exists:
            return "{'erro': 'e-mail já cadastrado no sistema'}"
        else:
            data = await users_collection.insert_one(jsonable_encoder(user))
            if data.inserted_id:
                return await get_user(users_collection, data.inserted_id)
    except Exception as e:
        return f'create_user.error: {e}'


async def get_user(users_collection, user_id):
    try:
        user = await users_collection.find_one({'_id': ObjectId(user_id)})
        if user:
            return json.loads(json_util.dumps(user))
    except Exception as e:
        return f'get_user.error: {e}'
        

async def get_user_by_email(users_collection, email):
    try:
        user = await users_collection.find_one({'email': email})
        if user:
            return json.loads(json_util.dumps(user))
    except Exception as e:
        return f'get_user.error: {e}'
        
        
async def get_users(users_collection, skip, limit):
    try:
        user_cursor = users_collection.find().skip(int(skip)).limit(int(limit))
        users = await user_cursor.to_list(length=int(limit))
        return json.loads(json_util.dumps(users))
    except Exception as e:
        return f'get_users.error: {e}'


async def update_user(users_collection, user_id, pwd):
    data = jsonable_encoder(pwd)
    try:
        user = await users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'password': data['password']}}
        )
        if user.modified_count:
            return True, user.modified_count
        return False, 0
    except Exception as e:
        return f'update_user.error: {e}'


async def delete_user(users_collection, user_id):
    try:
        user = await users_collection.delete_one(
            {'_id': ObjectId(user_id)}
        )
        if user.deleted_count:
            return {'status': 'User deleted'}
    except Exception as e:
        return f'delete_user.error: {e}'
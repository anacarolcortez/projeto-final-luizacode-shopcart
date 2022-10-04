from fastapi.encoders import jsonable_encoder
from bson import json_util
import json

async def find_cart_by_email(shopcarts_collection, email):
    try:
        shopcart = await shopcarts_collection.find_one({'email': email})
        if shopcart is not None:
            return json.loads(json_util.dumps(shopcart))
    except Exception as e:
        return f'find_cart_by_email.error: {e}'

async def update_cart(shopcarts_collection, email, shopcart):
    try:
        pass
    except:
        pass

async def insert_cart(shopcarts_collection, email, shopcart):
    try:
        data = await shopcarts_collection.insert_one(jsonable_encoder(shopcart))
        pass
    except:
        pass
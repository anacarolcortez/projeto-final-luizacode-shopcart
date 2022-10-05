from fastapi.encoders import jsonable_encoder
from bson import json_util
import json

async def find_opened_cart(shopcarts_collection, email):
    shopcart = await shopcarts_collection.find_one({'client.email': email, 'is_open': True})
    if shopcart is not None:
        return json.loads(json_util.dumps(shopcart))
    return None

async def update_opened_cart(shopcarts_collection, email, shopcart):
    cart = await shopcarts_collection.update_one(
        {'client.email': email},
        {'$set': shopcart}
    )
    if cart.modified_count:
        return json.loads(json_util.dumps(cart))
    return None

async def insert_cart(shopcarts_collection, shopcart):
    cart = await shopcarts_collection.insert_one(jsonable_encoder(shopcart))
    if cart.inserted_id:
        return await find_cart_by_id(shopcarts_collection, cart.inserted_id)
    return None

async def find_cart_by_id(shopcarts_collection, id):
    shopcart = await shopcarts_collection.find_one({'_id': id})
    if shopcart is not None:
        return json.loads(json_util.dumps(shopcart))
    return None
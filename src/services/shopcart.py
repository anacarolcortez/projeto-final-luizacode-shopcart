import logging
from fastapi.encoders import jsonable_encoder
from bson import json_util
import json

async def find_opened_cart(shopcarts_collection, email):
    shopcart = await shopcarts_collection.find_one({'client.email': email, 'is_open': True})
    if shopcart is not None:
        return json.loads(json_util.dumps(shopcart))
    return None


async def find_closed_cart(shopcarts_collection, email, skip, limit):
    shopcart_cursor = shopcarts_collection.find({'client.email': email, 'is_open': False}).skip(int(skip)).limit(int(skip))
    shopcarts = await shopcart_cursor.to_list(length=limit)
    return json.loads(json_util.dumps(shopcarts))


async def update_opened_cart(shopcarts_collection, email, new_quantity, new_value):
    cart = await shopcarts_collection.update_one(
        {'client.email': email},
        {'$set': {'quantity_cart': new_quantity, 'value': new_value}}
    )
    if cart.modified_count:
        return await find_opened_cart(shopcarts_collection, email)
    raise Exception("Erro ao atualizar o carrinho")


async def update_opened_cart_insert_new_product(shopcarts_collection, email, product, new_quantity, new_value ):
    cart = await shopcarts_collection.update_one(
        {'client.email': email}, 
        {'$addToSet': {'products': [product]}, 
        '$set': {'quantity_cart': new_quantity, 'value': new_value}}
    )
    if cart.modified_count:
        return await find_opened_cart(shopcarts_collection, email)
    raise Exception("Erro ao atualizar o novo produto no carrinho")


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


async def find_product_in_cart(shopcarts_collection, email, code):
    product = await shopcarts_collection.find_one(
        {"client.email": email, 
        "products.code": code}
    )
    if product is not None:
        return True
    return False


async def update_cart_to_closed(shopcarts_collection, email):
    cart = await shopcarts_collection.update_one(
        {'client.email': email},
        {'$set': {'is_open': False}}
    )
    if cart.modified_count:
        return {'status': 'OK. Carrinho fechado'}
    return None

    #como retornar o resultado final do carrinho fechado. 
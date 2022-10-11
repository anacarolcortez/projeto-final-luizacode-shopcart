from numbers import Number
from fastapi.encoders import jsonable_encoder
from bson import json_util
import json


async def find_opened_cart(shopcarts_collection, email):
    shopcart = await shopcarts_collection.find_one({'client.email': email, 'is_open': True})
    if shopcart is not None:
        return json.loads(json_util.dumps(shopcart))
    return None


async def find_closed_cart(shopcarts_collection, email, skip, limit):
    shopcart_cursor = shopcarts_collection.find(
        {'client.email': email, 'is_open': False}).skip(int(skip)).limit(int(skip))
    shopcarts = await shopcart_cursor.to_list(length=int(limit))
    return json.loads(json_util.dumps(shopcarts))


async def update_opened_cart(shopcarts_collection, email, new_quantity, new_value):
    cart = await shopcarts_collection.update_one(
        {'client.email': email},
        {'$set': {'quantity_cart': new_quantity, 'value': new_value}}
    )
    if cart.modified_count:
        return await find_opened_cart(shopcarts_collection, email)
    raise Exception("Erro ao atualizar o carrinho")


async def update_opened_cart_insert_new_product(shopcarts_collection, email, product):
    cart = await shopcarts_collection.update_one(
        {'client.email': email, 'is_open': True},
        {'$addToSet': {'products': product}}
    )
    if cart.modified_count:
        return True
    raise Exception("Erro ao inserir o novo produto no carrinho")


async def insert_cart(shopcarts_collection, shopcart):
    cart = await shopcarts_collection.insert_one(jsonable_encoder(shopcart))#
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
        {"client.email": email, "products.code": code, "is_open": True}
    )
    if product is not None:
        return True
    return False


async def update_cart_to_closed(shopcarts_collection, email):
    cart = await shopcarts_collection.update_one(
        {'client.email': email, 'is_open': True},
        {'$set': {'is_open': False}}
    )
    if cart.modified_count:
        opened_cart = await find_closed_cart(shopcarts_collection, email, 0, 10)
        if opened_cart is not None:
            return opened_cart
        raise Exception("Erro ao fechar carrinho")
    return None


async def update_product_quantity(shopcarts_collection, email, code, quantity):
    cart = await shopcarts_collection.update_one(
        {'client.email': email, 'is_open': True, 'products.code': code},
        {'$inc': {'products.$.quantity': quantity}}
    )
    if cart.modified_count:
        return True
    return False


async def update_cart_quantity_and_value(shopcarts_collection, email):
    total_value, total_quantity = await get_total_quantity_and_value(shopcarts_collection, email)
    if total_value is not None and total_quantity is not None:
        cart = await shopcarts_collection.update_one(
            {'client.email': email, 'is_open': True},
            {'$set': {'quantity_cart': total_quantity, 'value': total_value}}
        )
        if cart.modified_count:
            opened_cart = await find_opened_cart(shopcarts_collection, email)
            if opened_cart:
                return opened_cart
    raise Exception("Erro ao atualizar totais do carrinho")   


async def get_total_quantity_and_value(shopcarts_collection, email):
    data_cursor = shopcarts_collection.aggregate([
        {"$match": {"client.email": email, "is_open": True}},
        {"$unwind": "$products"},
        {"$group": {
            "_id": "client.email",
            "total_price": {
                "$sum": {
                    "$multiply": ["$products.price", "$products.quantity"]
                }
            },
            "total_quantity": {
                "$sum": "$products.quantity"
            },
        }}
    ])
    if data_cursor is not None:
        async for data in data_cursor: 
            return data["total_price"], data["total_quantity"]
    else:
        return None


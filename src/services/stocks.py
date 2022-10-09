from bson import ObjectId
from bson import json_util
from fastapi.encoders import jsonable_encoder
import json


async def create_stock(stocks_collection, stock_data):
    data = jsonable_encoder(stock_data)
    stock = await stocks_collection.insert_one(data)
    if stock.inserted_id:
        return await find_product_stock(stocks_collection, stock.inserted_id)
    return None


async def find_product_stock(stocks_collection, id):
    stock = await stocks_collection.find_one({'_id': ObjectId(id)})
    if stock is not None:
        return json.loads(json_util.dumps(stock))
    return None


async def find_product_quantity_stock(stocks_collection, code):
    stock = await stocks_collection.find_one({'product.code': code})
    if stock is not None:
        return stock['stock_quantity']
    return 0

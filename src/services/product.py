from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json

from server.database import db
products_collection = db.products_collection

async def find_one_product_by_id(product_id):
    product = await products_collection.find_one({'_id': ObjectId(product_id)})
    if product is not None:
        return json.loads(json_util.dumps(product))
    else:
        return None
    
    
async def find_one_product_by_code(code):
    product = await products_collection.find_one({'code': code})
    if product is not None:
        return json.loads(json_util.dumps(product))
    else:
        return None
     
     
async def find_one_product_by_name(name):
    product = await products_collection.find_one({'name': name})
    if product is not None:
        return json.loads(json_util.dumps(product))
    else:
        return None
    
    
async def insert_new_product(product):
    data = await products_collection.insert_one(product)
    if data.inserted_id:
        return await find_one_product_by_id(data.inserted_id)
    raise Exception("Erro ao cadastrar produto")


async def get_products_list(skip, limit):
    products_cursor = products_collection.find().skip(int(skip)).limit(int(limit))
    if products_cursor:
        clients = await products_cursor.to_list(length=int(limit))
        return json.loads(json_util.dumps(clients))
    else:
        return None


async def update_product_info(code, product_updated):
    product = await products_collection.update_one(
        {'code': code},
        {'$set': product_updated}
        )
    if product.modified_count:
        return await find_one_product_by_code(code)
    raise Exception("Erro ao atualizar produto")
    

async def delete_product_by_code(code):
    product = await products_collection.delete_one(
        {'code': code}
        )
    if product.deleted_count:
            return {'status': 'Produto deletado com sucesso'}
    raise Exception("Erro ao deletar produto")
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json


async def find_one_product_by_id(products_collection, product_id):
    product = await products_collection.find_one({'_id': ObjectId(product_id)})
    if product is not None:
        return json.loads(json_util.dumps(product))
    else:
        return None
    
    
async def find_one_product_by_code(products_collection, code):
    product = await products_collection.find_one({'code': code})
    if product is not None:
        return json.loads(json_util.dumps(product))
    else:
        return None
     
     
async def find_one_product_by_name(products_collection, name):
    product = await products_collection.find_one({'name': name})
    if product is not None:
        return json.loads(json_util.dumps(product))
    else:
        return None
    
    
async def insert_new_product(products_collection, product):
    data = await products_collection.insert_one(product)
    if data.inserted_id:
        return await find_one_product_by_id(products_collection, data.inserted_id)
    raise Exception("Erro ao cadastrar produto")


async def get_products_list(products_collection, skip, limit):
    products_cursor = products_collection.find().skip(int(skip)).limit(int(limit))
    if products_cursor:
        clients = await products_cursor.to_list(length=int(limit))
        return json.loads(json_util.dumps(clients))
    else:
        return None


async def update_product_info(products_collection, code, product_updated):
    product = await products_collection.update_one(
        {'code': code},
        {'$set': product_updated}
        )
    if product.modified_count:
        return await find_one_product_by_code(products_collection, code)
    raise Exception("Erro ao atualizar produto")
    

async def delete_product_by_code(products_collection, code):
    product = await products_collection.delete_one(
        {'code': code}
        )
    if product.deleted_count:
            return {'status': 'Produto deletado com sucesso'}
    raise Exception("Erro ao deletar produto")
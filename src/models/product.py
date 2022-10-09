from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json

from src.services.product import find_one_product_by_code, insert_new_product, find_one_product_by_name, get_products_list

async def create_product(products_collection, product):
    try:
        already_exists = await find_one_product_by_code(products_collection, product.code)
        if already_exists is not None:
            raise Exception("Um produto com este código já está cadastrado no sistema")
        else:
            return await insert_new_product(products_collection, jsonable_encoder(product))
    except Exception as e:
        return f'create_product.error: {e}'


async def get_product_by_code(products_collection, code):
    try:
        product_code = await find_one_product_by_code(products_collection, code)
        if product_code is not None:
            return json.loads(json_util.dumps(product_code))
        else:
            raise Exception("Produto não encontrado")
    except Exception as e:
        return f'get_product_by_code.error: {e}'  
    
    
async def get_product_by_name(products_collection, name):
    try:
        product_name = await find_one_product_by_name(products_collection, name)
        if product_name is not None:
            return json.loads(json_util.dumps(product_name))
        else:
            raise Exception("Producto não encontrado")
    except Exception as e:
        return f'get_product_by_name.error: {e}'  


        
async def get_all_products(products_collection, skip, limit):
    try:
        return await get_products_list(products_collection, skip, limit)
    except Exception as e:
        return f'get_all_products.error: {e}'
    
    

async def update_product(products_collection, code, name):
    data = jsonable_encoder(name)
    try:
        product = await products_collection.update_one(
            {'code': code},
            {'$set': {'name': data['name']}}
        )
        if product.modified_count:
            return True, product.modified_count
        return False, 0
    except Exception as e:
        return f'update_product.error: {e}'


async def delete_product(products_collection, code):
    try:
        product = await products_collection.delete_one(
            {'code': code}
        )
        if product.deleted_count:
            return {'status': 'Product deleted'}
    except Exception as e:
        return f'delete_product.error: {e}'
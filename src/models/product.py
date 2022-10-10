from fastapi.encoders import jsonable_encoder
from bson import json_util
import json

from src.services.product import (
    find_one_product_by_code, insert_new_product, find_one_product_by_name, 
    get_products_list, delete_product_by_code, update_product_info
)

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
            raise Exception("Produto não encontrado")
    except Exception as e:
        return f'get_product_by_name.error: {e}'  


        
async def get_all_products(products_collection, skip, limit):
    try:
        return await get_products_list(products_collection, skip, limit)
    except Exception as e:
        return f'get_all_products.error: {e}'
    
    

async def update_product(products_collection, code, update_product):
    try:
        return await update_product_info(products_collection, code, update_product)
    except Exception as e:
        return f'update_product.error: {e}'



async def delete_product(products_collection, code):
    try:
        return await delete_product_by_code(products_collection, code)
    except Exception as e:
        return f'delete_product.error: {e}'
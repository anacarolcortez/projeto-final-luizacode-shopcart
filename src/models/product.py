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
            product_data = jsonable_encoder(product)
            is_over_one_cent = await validate_product_price(product_data["price"])
            if is_over_one_cent:
                return await insert_new_product(products_collection, product_data)
            else:
                raise Exception("Informe um preço maior que R$ 0.01")
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
        product_data = jsonable_encoder(update_product)
        is_over_one_cent = await validate_product_price(product_data["price"])
        if is_over_one_cent:
            return await update_product_info(products_collection, code, product_data)
        else:
            raise Exception("Informe um preço maior que R$ 0.01")
    except Exception as e:
        return f'update_product.error: {e}'


async def delete_product(products_collection, code):
    try:
        return await delete_product_by_code(products_collection, code)
    except Exception as e:
        return f'delete_product.error: {e}'
    
    
async def validate_product_price(product_price):
    return product_price > 0.01
        
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json

async def create_product(products_collection, product):
    try:
        already_exists = await get_product_by_code(products_collection, product.code)
        if already_exists:
            return "{'erro': 'código já cadastrado no sistema'}"
        else:
            data = await products_collection.insert_one(jsonable_encoder(product))
            if data.inserted_id:
                return await get_product(products_collection, data.inserted_id)
    except Exception as e:
        return f'create_product.error: {e}'


async def get_product(products_collection, product_id):
    try:
        product = await products_collection.find_one({'_id': ObjectId(product_id)})
        if product:
            return json.loads(json_util.dumps(product))
    except Exception as e:
        return f'get_product.error: {e}'
        

async def get_product_by_code(products_collection, code):
    try:
        product = await products_collection.find_one({'code': code})
        if product:
            return product
    except Exception as e:
        return f'get_product.error: {e}'
    
async def get_product_by_name(products_collection, name):
    try:
        product = await products_collection.find_one({'name': name})
        if product:
            return product
    except Exception as e:
        return f'get_product.error: {e}'


        
async def get_products(products_collection, skip, limit):
    try:
        product_cursor = products_collection.find().skip(int(skip)).limit(int(limit))
        products = await product_cursor.to_list(length=int(limit))
        return json.loads(json_util.dumps(products))
    except Exception as e:
        return f'get_products.error: {e}'


async def update_product(products_collection, code, nam):
    data = jsonable_encoder(nam)
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
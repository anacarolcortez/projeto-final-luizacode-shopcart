from ast import IsNot
from itertools import product
from xmlrpc import client
from src.models.clients import get_client_by_email
from src.models.product import get_product_by_code
from src.schemas.shopcart import ShopcartSchema
from fastapi.encoders import jsonable_encoder

from src.services.shopcart import find_cart_by_email, update_cart


async def create_shopcart(shopcarts_collection, clients_collection, products_collection, shopcart, email, code):
    try:
        client_data = await get_client_by_email(clients_collection, email)
        if type(client_data) == dict:
            if code is not None:
                product = await get_product_by_code(products_collection,code)
                if product is not None:
                    shopcart_data = ShopcartSchema(
                        client = client_data,
                        products = [product],
                        is_open = shopcart.is_open,
                        quantity = shopcart.quantity
                    )
                response = await insert_cart(jsonable_encoder(shopcart_data))
            
    except:
        pass

async def cart_handler(shopcarts_collection, email):
    response = await get_cart_by_email(shopcarts_collection,email)
    

    #validar quantidade do produto no estoque
    #modificar o estoque atual do produto
    #multiplicar quantidade x preço para ter o valor do carrinho
    ...

# criar função de consulta de carrinho pelo e-mail cliente(se tem carrinho aberto, adicionar os novos produtos, se não criar carrinho do zero)
async def get_cart_by_email(shopcarts_collection, email, shopcart):
    try:
        response = await find_cart_by_email(shopcarts_collection, email)
        if type(response) == dict:
            cart = await update_cart(shopcarts_collection, email, shopcart)
        else:
            cart = ...
            
    except Exception as e:
        return f'get_cart_by_email.error: {e}'


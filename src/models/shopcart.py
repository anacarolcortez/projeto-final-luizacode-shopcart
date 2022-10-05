from ast import IsNot
from itertools import product
from multiprocessing.connection import wait
from urllib import response
from xmlrpc import client
from src.models.clients import get_client_by_email
from src.models.product import get_product_by_code
from src.schemas.shopcart import ShopcartSchema
from fastapi.encoders import jsonable_encoder
from src.services.shopcart import find_cart_by_email, find_opened_cart, insert_cart, update_cart, update_opened_cart


async def create_shopcart(shopcarts_collection, clients_collection, products_collection, shopcart, email, code):
    try:
        client_data = await get_client_by_email(clients_collection, email)

        if client_data is None:
            raise Exception("Cliente não localizado") 
        product = await get_product_by_code(products_collection,code)

        if product is None:
            raise Exception("Produto não cadastrado")
        cart = await get_opened_cart(shopcarts_collection, email)

        if cart is None:
            # Chamar funções que validam quantidade de produtos no estoque
            shopcart_data = ShopcartSchema(
                        client = client_data,
                        products = [product],
                        is_open = True,
                        quantity_cart = product["quantity"],
                        value = product["quantity"] * product["price"]
                    )
            response = await insert_cart(jsonable_encoder(shopcart_data))
            if response is not None:
                return response
            raise Exception("Erro ao criar carrinho de compras")
        else:
            response = await update_opened_cart(shopcarts_collection, product)
            # Chamar funções de atualização de valor do carrinho e quantidade de produtos do carrinho
            if response is not None:
                return response
            raise Exception("Erro ao atualizar carrinho de compras")
    except Exception as e:
        return f'create_shopcart.error: {e}'

    ...

# criar função de consulta de carrinho pelo e-mail cliente(se tem carrinho aberto, adicionar os novos produtos, se não criar carrinho do zero)
async def get_opened_cart(shopcarts_collection, email, shopcart):
    try:
        return await find_opened_cart(shopcarts_collection, email)      
    except Exception as e:
        return f'get_opened_cart.error: {e}'

async def get_product_stock(product):
    return product["quantity"]

async def compare_product_quantity(cart_quantity, products_collection, product):
    product_quantity = await get_product_stock(products_collection, product)
    return product_quantity >= cart_quantity

async def quantity_cart(cart_quantity, product_quantity):
    return cart_quantity + product_quantity

async def value_cart(product_quantity, product_value,cart_value):
    cart_value += product_quantity * product_value
    return cart_value



    #validar quantidade do produto no estoque
    # comparar se o estoque é maior ou igual do que a quantidade solicitada pelo carrinho
    #modificar o estoque atual do produto
    #multiplicar quantidade x preço para ter o valor do carrinho


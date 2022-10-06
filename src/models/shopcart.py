from ast import IsNot
from itertools import product
from multiprocessing.connection import wait
from urllib import response
from xmlrpc import client
from src.models.clients import get_client_by_email
from src.models.product import get_product_by_code
from src.schemas.shopcart import ShopcartSchema, UpdateShopcartSchema
from fastapi.encoders import jsonable_encoder
from src.services.shopcart import find_opened_cart, find_product_in_cart, insert_cart, update_opened_cart


async def create_shopcart(shopcarts_collection, clients_collection, products_collection, email, code, new_cart):
    # receber a quantidade de produto a adicionar no carrinho
    try:
        client_data = await get_client_by_email(clients_collection, email)

        if client_data is None:
            raise Exception("Cliente não localizado")
        product = await get_product_by_code(products_collection, code)

        if product is None:
            raise Exception("Produto não cadastrado")
        cart = await get_opened_cart(shopcarts_collection, email)

        if cart is None:
            shopcart_data = ShopcartSchema(
                client=client_data,
                products=[product],
                is_open=True,
                quantity_cart=new_cart.quantity_cart,
                value=new_cart.quantity_cart * product["price"]
            )
            response = await insert_cart(shopcarts_collection, jsonable_encoder(shopcart_data))
            if response is not None:
                return response
            raise Exception("Erro ao criar carrinho de compras")
        else:
            return await update_cart(shopcarts_collection, email, product, cart, code, new_cart)
    except Exception as e:
        return f'create_shopcart.error: {e}'


async def update_cart(shopcarts_collection, email, product, cart, code, new_cart):
    # criar função:validar pelo codigo do produto se ele já existe no carrinho
    has_product = await find_product_in_cart(shopcarts_collection, email, code)
    if has_product:
        pass #criar um objeto que passa a quantidade e valor  
    else:
        shopcart_data = UpdateShopcartSchema(
            products=product,
            quantity_cart=quantity_cart(cart.quantity_cart, new_cart.quantity_cart),
            value=value_cart(new_cart.quantity_cart, product.price, cart.value)
        )
    response = await update_opened_cart(shopcarts_collection, email, shopcart_data)
    if response is not None:
        return response
    raise Exception("Erro ao atualizar carrinho de compras")


async def get_opened_cart(shopcarts_collection, email):
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


async def value_cart(product_quantity, product_value, cart_value):
    cart_value += product_quantity * product_value
    return cart_value

    # validar quantidade do produto no estoque
    # comparar se o estoque é maior ou igual do que a quantidade solicitada pelo carrinho
    # modificar o estoque atual do produto
    # multiplicar quantidade x preço para ter o valor do carrinho

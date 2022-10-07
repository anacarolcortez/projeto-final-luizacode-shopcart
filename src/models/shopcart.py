from logging import raiseExceptions
from src.models.clients import get_client_by_email
from src.models.product import get_product_by_code
from src.schemas.shopcart import ShopcartSchema, UpdateShopcartSchema
from fastapi.encoders import jsonable_encoder
from src.services.shopcart import find_closed_cart, find_opened_cart, find_product_in_cart, insert_cart, update_cart_to_closed, update_opened_cart, update_opened_cart_insert_new_product


async def validate_cart(shopcarts_collection, clients_collection, products_collection, email, code):
        client_data = await get_client_by_email(clients_collection, email)
        if client_data is None:
            raise Exception("Cliente não localizado")
        
        product_data = await get_product_by_code(products_collection, code)
        if product_data is None:
            raise Exception("Produto não cadastrado")
        
        cart_data = await get_opened_cart(shopcarts_collection, email)
        if type(cart_data) != dict:
            cart_data = None
                
        return client_data, product_data, cart_data
            

async def create_shopcart(shopcarts_collection, clients_collection, products_collection, email, code, new_cart):
    try:
        client_data, product_data, cart_data = await validate_cart(shopcarts_collection, clients_collection, products_collection, email, code)

        if cart_data is None:
            shopcart_data = ShopcartSchema(
                client=client_data,
                products=[product_data],
                is_open=True,
                quantity_cart= new_cart.quantity_cart,
                value=new_cart.quantity_cart * product_data["price"]
            )
            response = await insert_cart(shopcarts_collection, jsonable_encoder(shopcart_data))
            if response is not None:
                return response
            raise Exception("Erro ao criar carrinho de compras")
        else:
            raise Exception("Já existe um carrinho aberto com este produto. Atualize o carrinho para alterar suas informações")
    except Exception as e:
        return f'create_shopcart.error: {e}'


async def update_cart(shopcarts_collection, clients_collection, products_collection, email, code, new_cart):
    client_data, product_data, cart_data = await validate_cart(shopcarts_collection, clients_collection, products_collection, email, code)

    has_product = await find_product_in_cart(shopcarts_collection, client_data['email'], product_data['code'])
    if has_product:
        shopcart_data = UpdateShopcartSchema(
            quantity_cart = get_quantity_cart(cart_data['quantity_cart'], new_cart.quantity_cart),
            value = get_value_cart(new_cart.quantity_cart, product_data['price'], cart_data['value'])
        )
        response = await update_opened_cart(shopcarts_collection, email, shopcart_data)
    else:
        shopcart_data = UpdateShopcartSchema(
            products = product_data,
            quantity_cart = get_quantity_cart(cart_data['quantity_cart'], new_cart.quantity_cart),
            value = get_value_cart(new_cart.quantity_cart, product_data['price'], cart_data['value'])
        )
        response = await update_opened_cart_insert_new_product(shopcarts_collection, email, shopcart_data)
    if response is not None:
        return response
    raise Exception("Erro ao atualizar carrinho de compras")


async def get_opened_cart(shopcarts_collection, email):
    try:
        response = await find_opened_cart(shopcarts_collection, email)
        if response is not None:
            return response
        raise Exception("Não há carrinhos abertos para este cliente")
    except Exception as e:
        return f'get_opened_cart.error: {e}'


async def get_closed_cart(shopcarts_collection, email, skip, limit):
    try:
        response = await find_closed_cart(shopcarts_collection, email, skip, limit)
        if response is not None:
            return response
        raise Exception("Não há carrinhos fechados para este cliente")
    except Exception as e:
        return f'get_closed_cart.error: {e}'


async def put_closed_shopcart(shopcarts_collection, email):
    try:
        response = await update_cart_to_closed(shopcarts_collection, email)
        if response != None:
            return response
        raise Exception("Não há carrinho aberto para este cliente")
    except Exception as e:
        return f'put_closed_shopcart.error: {e}'


async def get_product_stock(product):
    return product["quantity"]


async def compare_product_quantity(cart_quantity, products_collection, product):
    product_quantity = await get_product_stock(products_collection, product)
    return product_quantity >= cart_quantity


async def get_quantity_cart(cart_quantity, product_quantity):
    return cart_quantity + product_quantity


async def get_value_cart(product_quantity, product_value, cart_value):
    cart_value += product_quantity * product_value
    return cart_value

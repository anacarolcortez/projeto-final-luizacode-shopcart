from src.models.clients import get_client_by_email
from src.models.product import get_product_by_code
from src.schemas.shopcart import ShopcartSchema
from fastapi.encoders import jsonable_encoder
from src.services.stocks import find_product_quantity_stock
from src.services.shopcart import (
    find_closed_cart, find_opened_cart, find_product_in_cart, insert_cart, 
    update_cart_to_closed, update_opened_cart, update_opened_cart_insert_new_product)


async def validate_cart(shopcarts_collection, clients_collection, products_collection, 
                        stocks_collection, email, code):
        client_data = await get_client_by_email(clients_collection, email)
        if client_data is None:
            raise Exception("Cliente não localizado")
        
        product_data = await get_product_by_code(products_collection, code)
        if product_data is None:
            raise Exception("Produto não cadastrado")
        
        stock_qt =  await find_product_quantity_stock(stocks_collection, code)
        
        cart_data = await get_opened_cart(shopcarts_collection, email)
        if type(cart_data) != dict:
            cart_data = None
                
        return client_data, product_data, stock_qt, cart_data
            

async def create_shopcart(shopcarts_collection, clients_collection, products_collection,
                          stocks_collection, email, code, insert_product):
    try:
        client_data, product_data, stock_qt, cart_data = await validate_cart(shopcarts_collection, clients_collection, 
                                                                             products_collection, stocks_collection,
                                                                             email, code)
        product_data["quantity"] = insert_product.quantity_product
        
        if not await has_stock_availability(product_data["quantity"], stock_qt):
            raise Exception("Quantidade insuficiente de estoque para este produto")
            
        if cart_data is None:
            shopcart_data = ShopcartSchema(
                client = client_data,
                products = [product_data],
                is_open = True,
                quantity_cart = insert_product.quantity_product,
                value = insert_product.quantity_product * product_data["price"]
            )
            response = await insert_cart(shopcarts_collection, jsonable_encoder(shopcart_data))
            if response is not None:
                return response
            raise Exception("Erro ao criar carrinho de compras")
        else:
            raise Exception("Já existe um carrinho aberto com este produto. Atualize o carrinho para alterar suas informações")
    except Exception as e:
        return f'create_shopcart.error: {e}'


async def update_cart(shopcarts_collection, clients_collection, products_collection, 
                      stocks_collection, email, code, new_produtc_qt):
    try:
        _, product_data, cart_data = await validate_cart(shopcarts_collection, clients_collection, 
                                                                   products_collection, stocks_collection,
                                                                   email, code)
        if cart_data is None:
            raise Exception("Este cliente não possui carrinhos abertos para serem atualizados")
        has_quantity = await has_stock_availability(new_produtc_qt.quantity_product, product_data)
        if not has_quantity:
            raise Exception("A quantidade de produtos solicitada não existe em estoque")    
        # validar: adicionar e remover a quantidade do produto dentro do carrinho
        new_quantity = await get_quantity_cart(cart_data["quantity_cart"], new_produtc_qt.quantity_product)
        new_value = await get_value_cart(new_produtc_qt.quantity_product, product_data["price"], cart_data["value"])
        cart_has_the_product = await find_product_in_cart(shopcarts_collection, email, code)
        if cart_has_the_product:
            return await update_opened_cart(shopcarts_collection, email, new_quantity, new_value)
        else:
            return await update_opened_cart_insert_new_product(shopcarts_collection, email, product_data, new_quantity, new_value)
    except Exception as e:
        return f'update_cart.error: {e}'


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


async def has_stock_availability(product_quantity, stock_quantity):
    return stock_quantity >= product_quantity


async def get_quantity_cart(cart_quantity, insert_quantity):
    return cart_quantity + insert_quantity


async def get_value_cart(insert_quantity, product_value, cart_value):
    cart_value += insert_quantity * product_value
    return cart_value

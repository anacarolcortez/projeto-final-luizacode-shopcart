from operator import neg
from src.models.clients import get_client_by_email
from src.models.product import get_product_by_code
from src.schemas.shopcart import ShopcartSchema
from fastapi.encoders import jsonable_encoder
from src.services.stocks import find_product_quantity_stock
from src.services.shopcart import (
    find_closed_cart, find_opened_cart, find_product_in_cart, insert_cart, update_cart_quantity_and_value, 
    update_cart_to_closed, update_opened_cart_insert_new_product, update_product_quantity)


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
        if insert_product.quantity_product > 0:
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
                raise Exception("Já existe um carrinho aberto para este cliente. Atualize ou feche o carrinho")
        raise Exception("Informe uma quantidade válida")
    except Exception as e:
        return f'create_shopcart.error: {e}'


async def update_cart(shopcarts_collection, clients_collection, products_collection, 
                      stocks_collection, email, code, insert_product):
    try:
        if insert_product.quantity_product <= 0:
            raise Exception("Informe um valor maior que zero")
        
        _, product_data, stock_qt, cart_data = await validate_cart(shopcarts_collection, clients_collection, 
                                                                             products_collection, stocks_collection,
                                                                             email, code)
        
        if cart_data is None:
            raise Exception("Este cliente não possui carrinhos abertos para serem atualizados")
        

        if not await has_stock_availability(insert_product.quantity_product, stock_qt):
            raise Exception("Quantidade insuficiente de estoque para este produto")

        cart_has_the_product = await find_product_in_cart(shopcarts_collection, email, code)       
        if cart_has_the_product:
            await update_product_quantity(shopcarts_collection, email, code, insert_product.quantity_product)
        else:
            product_data["quantity"] = insert_product.quantity_product
            del product_data['_id']
            await update_opened_cart_insert_new_product(shopcarts_collection, email, product_data)
        return await update_cart_quantity_and_value(shopcarts_collection, email)
    
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


async def update_cart_delete_item(shopcarts_collection, clients_collection, 
                                  products_collection, stocks_collection, email, code,
                                  delete_product_qt):
    
    try:
        if delete_product_qt.quantity_product <= 0:
            raise Exception("Informe um valor maior que zero")
        
        _, product_data, _, cart_data = await validate_cart(shopcarts_collection, clients_collection, 
                                                                                    products_collection, stocks_collection,
                                                                                    email, code)
        if cart_data is None:
            raise Exception("Este cliente não possui carrinhos abertos para serem atualizados")
        
        cart_has_the_product = await find_product_in_cart(shopcarts_collection, email, code)       
        if not cart_has_the_product:
            raise Exception("Este produto não está inserido no carrinho")
        
        product_quantity_in_cart = await get_product_quantity_in_cart(cart_data, code)
        has_product_qt = await has_stock_availability(delete_product_qt.quantity_product, product_quantity_in_cart)
        if not has_product_qt:
            raise Exception("Quantidade a ser excluída excede a quantidade existente no carrinho")
        
        deleted_qt = await update_product_quantity(shopcarts_collection, email, code, neg(delete_product_qt.quantity_product))
        if deleted_qt:
            return await update_cart_quantity_and_value(shopcarts_collection, email)
        else:    
            raise Exception("Erro ao excluir itens do carrinho")
    
    except Exception as e:
        return f'update_cart_delete_item.error: {e}'
    

async def get_product_quantity_in_cart(cart_data, code):
    for product in cart_data["products"]:
        if product["code"] == code:
            return product["quantity"]
    return 0
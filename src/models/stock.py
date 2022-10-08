from src.models.product import get_product_by_code


async def create_product_stock(products_collection, code, stock):
    try:
        product = await get_product_by_code(products_collection, code)
        if type(product) == dict:
           pass 
    except Exception as e:
        return f"create_product_stock.error: {e}"
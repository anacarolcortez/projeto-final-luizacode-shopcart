from src.models.product import get_product_by_code
from src.schemas.stock import StockSchema
from src.services.stocks import create_stock


async def create_product_stock(stocks_collection, products_collection, code, stock):
    try:
        product = await get_product_by_code(products_collection, code)
        if type(product) == dict:
            stock_schema = StockSchema(
                product = product, 
                stock_quantity = stock.stock_quantity 
            )
            stock_data = await create_stock(stocks_collection, stock_schema)
            if stock_data is not None:
                return stock_data
            raise Exception("Erro ao cadastrar estoque para esse produto")
    except Exception as e:
        return f"create_product_stock.error: {e}"

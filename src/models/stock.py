from src.models.product import get_product_by_code
from src.schemas.stock import StockSchema
from src.services.stocks import create_stock


async def create_product_stock(code, stock):
    try:
        if stock.stock_quantity <= 0:
            raise Exception(
                "Cadastre uma quantidade válida para o estoque do produto")
        product = await get_product_by_code(code)
        if type(product) == dict:
            stock_schema = StockSchema(
                product=product,
                stock_quantity=stock.stock_quantity
            )
            stock_data = await create_stock(stock_schema)
            if stock_data is not None:
                return stock_data
            raise Exception("Erro ao cadastrar estoque para esse produto")
    except Exception as e:
        return f"create_product_stock.error: {e}"

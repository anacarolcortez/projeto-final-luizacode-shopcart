from motor.motor_asyncio import AsyncIOMotorClient
from os import environ
from dotenv import load_dotenv
load_dotenv()


class DataBase():
    client = AsyncIOMotorClient(environ.get("DATABASE_URI"))
    db = client['luizacode5']

    users_collection = db['users']
    address_collection = db['address']
    user_address_collection = db['user_address']
    products_collection = db['products']
    orders_collection = db['orders']
    order_item_collection = db['order_item']


db = DataBase()

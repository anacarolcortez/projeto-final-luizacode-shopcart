from motor.motor_asyncio import AsyncIOMotorClient
from os import environ
from dotenv import load_dotenv
load_dotenv()


class DataBase():
    client = AsyncIOMotorClient(environ.get("DATABASE_URI"))
    db = client['luizacode5']

    users_collection = db['users']
    clients_collection = db['clients']
    address_collection = db['address']
    delivery_collection = db['delivery']
    products_collection = db['products']
    shopcarts_collection = db['shopcarts']


db = DataBase()

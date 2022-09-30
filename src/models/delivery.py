from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json

from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson import json_util
import json


async def create_user_delivery_address(delivery_collection, clients_collection,
                                       address_collection, email, zipcode, address):
    pass


async def get_delivery_address_by_email(email):
    pass


async def delete_delivery_address_by_zipcode(zipcode, email):
    pass


async def get_user_and_address(clients_collection, address_collection, email, zipcode):
    #user = await get_user(users_collection, user_id)
    #address = await get_address(address_collection, address_id)
    #return user, address
    pass

#upsert address info (complement)
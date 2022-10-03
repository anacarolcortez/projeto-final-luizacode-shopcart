import pytest
import pytest_asyncio
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from src.controllers import clients

test_app = TestClient(app)
PREFIX = clients.router.prefix
clients_collection = clients.clients_collection


#Setting Test Environment
@pytest_asyncio.fixture
async def clear_collection():
    await clients_collection.delete_many({})
    return None


#Tests
@pytest.mark.asyncio
async def test_create_client_correctly(clear_collection):
    assert clear_collection is None

    dummyclient = {
        "name": "Daenerys Targaryen",
        "email": "motherofdragons@got.com",
        "cpf": "12345678910"
    }
    response = test_app.post(PREFIX + "/", json=dummyclient)
    assert response.status_code == status.HTTP_200_OK
    
    dummyclient_data = response.json()
    assert dummyclient['name'] in dummyclient_data
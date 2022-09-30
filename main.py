import uvicorn
from fastapi import FastAPI
from src.controllers import address, clients, delivery, users, products

app = FastAPI()
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(address.router)
app.include_router(delivery.router)
app.include_router(products.router)



if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True, access_log=False)

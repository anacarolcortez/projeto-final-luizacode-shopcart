import uvicorn
from fastapi import FastAPI
from src.controllers import users

app = FastAPI()
app.include_router(users.router)
# app.include_router(products.router)
# app.include_router(user_address.router)
# app.include_router(address.router)
# app.include_router(orders.router)
# app.include_router(order_item.router)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True, access_log=False)

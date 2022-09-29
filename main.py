import uvicorn
from fastapi import FastAPI
from src.controllers import address, users

app = FastAPI()
app.include_router(users.router)
app.include_router(address.router)
# app.include_router(delivery.router)



if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True, access_log=False)

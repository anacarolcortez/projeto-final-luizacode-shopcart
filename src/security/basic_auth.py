import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


from server.database import db
users_collection = db.users_collection


security = HTTPBasic()


async def validate_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    current_username = credentials.username.encode("utf8")
    current_password = credentials.password.encode("utf8")
    
    usr, pwd = await get_user_credentials(current_username)

    is_correct_username = secrets.compare_digest(
        current_username, usr
    )

    is_correct_password = secrets.compare_digest(
        current_password, pwd
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return usr.decode("utf8")


async def get_user_credentials(current_username):
    current_username = current_username.decode("utf8")
    response = await users_collection.find_one({'email': current_username})
    if response is not None:
        is_active = response["is_active"]
        if is_active:
            return response["email"].encode("utf8"), response["password"].encode("utf8")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo",
            headers={"WWW-Authenticate": "Basic"},
        )
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não cadastrado no sistema",
            headers={"WWW-Authenticate": "Basic"},
        )
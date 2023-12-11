from sqlite3 import Date
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .. import schemas
from fastapi import FastAPI , Response , status , HTTPException , Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_user_token (data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verifyToken(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        id_str = str(user_id)
        token_data = schemas.TokenData(id=id_str)
    except JWTError:
        raise credentials_exception
    return token_data

    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not verify the credentials", headers={"WWW-Authenticate":"Bearer"})

    return verifyToken(token, credentials_exception)

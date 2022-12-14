from cmath import e
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app1 import schemas, database, models 
from .config import settings

load_dotenv()

scrt_ky = os.getenv("SECRET_KEY")
algrthm = os.getenv("ALGORITHM")
acces_time_tkn = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# SECRET KEY
# Algorithm
# expiration time- foirevr time for examples

SECRET_KEY = scrt_ky
ALGORITHM = algrthm
ACCESS_TOKEN_EXPIRE_MINUTES = acces_time_tkn

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
    
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'})

    token = verify_access_token(token, credentials_exception=credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user




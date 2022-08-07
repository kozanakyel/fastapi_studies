from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
#def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db), ):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), ):

    #user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail=f'Invalid Credentials')

    hashed_user_password = utils.hash(user.password)  # bu video da yoktu gerekli hata veriryor
    if not utils.verify(plain_password=user_credentials.password, hashed_password=hashed_user_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail=f'Invalid Credentials')

    access_token =oauth2.create_access_token(data={"user_id": user.id})

    #create token
    #return token
    return {'access_token': access_token, 'token_type': 'bearer'}

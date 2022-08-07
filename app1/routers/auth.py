from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db), ):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Invalid Credentials')

    hashed_user_password = utils.hash(user.password)  # bu video da yoktu gerekli hata veriryor
    if not utils.verify(plain_password=user_credentials.password, hashed_password=hashed_user_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f'Invalid Credentials')

    #create token
    #return token
    return {'token': 'implement token'}

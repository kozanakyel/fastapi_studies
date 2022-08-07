from passlib.context import CryptContext 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(passworrd: str):
    return pwd_context.hash(passworrd)

def verify(plain_password, hashed_password):
    print('plain cre hash', plain_password, 'user has', hashed_password)
    print('eslesme: ', pwd_context.verify(plain_password, hashed_password))
    return pwd_context.verify(plain_password, hashed_password)
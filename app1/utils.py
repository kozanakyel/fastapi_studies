from passlib.context import CryptContext 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(passworrd: str):
    return pwd_context.hash(passworrd)
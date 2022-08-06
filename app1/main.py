from fastapi import FastAPI
from . import models
from .database import engine
from dotenv import load_dotenv
import os
from .routers import post, user


load_dotenv()

db = os.getenv("DB")
host = os.getenv("HOST")
password = os.getenv("PSWD")
userDB = os.getenv("USER")

print(password)

models.Base.metadata.create_all(bind=engine) # this codes create tables

app = FastAPI()

"""
while True:    
    try:
        conn = psycopg2.connect(host=host, database=db, 
                            user=userDB, password=password, 
                            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successfull')
        break
    except Exception as error:
        print("connetcion failedd error--------------")
        print('Error:', error)
        time.sleep(2)
"""



app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome my web api"}








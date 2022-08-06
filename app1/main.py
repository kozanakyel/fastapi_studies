from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
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








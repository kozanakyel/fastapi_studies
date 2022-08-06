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


    
my_post = [{'title':'title of post 1', 'content': 'content 0f 1', 'id': 1},
           {'title':'title pizza', 'content': 'content 0f pizza', 'id': 2}]


def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for index, post in enumerate(my_post):
        if post['id'] == id:
            return index

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome my web api"}








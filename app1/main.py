from fastapi import FastAPI
from . import models
from .database import engine
from dotenv import load_dotenv
import os
from .routers import post, user, auth


load_dotenv()

models.Base.metadata.create_all(bind=engine) # this codes create tables

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome my web api"}








from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine) # this codes create tables

app = FastAPI()


    
  
while True:    
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', 
                            user='postgres', password='1613', 
                            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successfull')
        break
    except Exception as error:
        print("connetcion failedd error--------------")
        print('Error:', error)
        time.sleep(2)

    
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

@app.get("/")
def root():
    return {"message": "Welcome my web api"}


@app.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post('/posts', response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 1000000)
    #my_post.append(post_dict)
    
    ##never do!  cursor.execute(f"  ") this tecnically work bur some weird occured nor reccommended
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)  RETURNING * """, 
    #               (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() # keep in mind it is necessary for all insert operations
    
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # for returning *, sql alchemy model
            
    return new_post
# title str, content str

#YOU HAVE TO CAREFULL
    """
@app.get('/posts/latest') # error because fastapi lokk first match
def get_latest_post():
    post = my_post[len(my_post)-1]
    return {'detail': post}

    """


@app.get('/posts/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)): # automatically converted from frontend
    #print(type(id))  # there is an error type convertions
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    #print(test_post)
    
    #post = find_post(id)
    #print(post)

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f'post with id: {id} was not found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
    return post



@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """,(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    # deleting post
    # find thje index in the array that has required id
    # my_post.pop(index)
   
    # index = find_index_post(id)

    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')
    
    post.delete(synchronize_session=False)
    db.commit()

    # my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s returning * """, 
      #             (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_post[index] = post_dict
    return post_query.first()



@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


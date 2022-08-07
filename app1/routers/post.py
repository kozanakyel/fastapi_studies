from typing import List

from app1 import oauth2
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts'] # for the swagger divided
)

@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post('/', response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 1000000)
    #my_post.append(post_dict)
    
    ##never do!  cursor.execute(f"  ") this tecnically work bur some weird occured nor reccommended
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)  RETURNING * """, 
    #               (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() # keep in mind it is necessary for all insert operations
    
    print(current_user.email)
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


@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # automatically converted from frontend
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



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
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


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
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
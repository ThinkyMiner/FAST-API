from click import get_current_context
from fastapi.security import OAuth2
from . import oauth2
from app.routers.oauth2 import get_current_user
from .. import models, schemas, utils
from fastapi import Body, FastAPI , Response , status , HTTPException , Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal,get_db
from typing import List

router = APIRouter()

@router.get("/posts", response_model=List[schemas.Post])
def post(db : Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0):
    # the common sql code used is in the 2 lines lower
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).limit(limit).offset(skip).all()
    return posts



@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)# or to change the status code we can just pass another attribute next to posts as status_code=status.HTTP....
def create_post(post : schemas.CreatePost, db : Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title , post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(user_id)
    new_post = models.Post(**post.dict(), owner_id = user_id.id) # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
# the things we actually require. -> title str, content str 



@router.get("/posts/{id}", response_model=schemas.Post)
def indexPost(id: int , response: Response, db : Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""" , (str(id)))
    # indexed_post = cursor.fetchone()
    # print(indexed_post)
    print(limit)
    indexed_post = db.query(models.Post).filter(models.Post.id == int(id)).first()
    
    if not indexed_post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id : {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} was not found")
    return indexed_post



@router.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()#very important line of code remember this
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post = deleted_post.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} does not exist")
    if post.owner_id != user_id.id: # type: ignore
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    else:
        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post:schemas.CreatePost, db : Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """ , (post.title , post.content , post.published , str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    posts = db.query(models.Post).filter(models.Post.id == id)
    updated_post = posts.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} does not exist")
    if updated_post.owner_id != user_id.id: # type: ignore
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    posts.update(post.dict()) # type: ignore
    db.commit()
    return posts.first()
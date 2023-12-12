
from app.routers import oauth2
from .. import models, schemas
from fastapi import Response , status , HTTPException , Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter()

@router.get("/posts", response_model=List[schemas.Post])
def post(db : Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0):
    posts = db.query(models.Post).limit(limit).offset(skip).all()
    return posts



@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)# or to change the status code we can just pass another attribute next to posts as status_code=status.HTTP....
def create_post(post : schemas.CreatePost, db : Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict(), owner_id = user_id.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
# the things we actually require. -> title str, content str 



@router.get("/posts/{id}", response_model=schemas.Post)
def indexPost(id: int , response: Response, db : Session = Depends(get_db)):
    indexed_post = db.query(models.Post).filter(models.Post.id == int(id)).first()
    if not indexed_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} was not found")
    return indexed_post



@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter_by(id=id).first()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {user_id.id} does not exist")
    if deleted_post.owner_id is not int(user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(deleted_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post:schemas.CreatePost, db : Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == id)
    updated_post = posts.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} does not exist")
    if updated_post.owner_id != int(user_id.id): # type: ignore
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    posts.update(post.dict()) # type: ignore
    db.commit()
    return posts.first()
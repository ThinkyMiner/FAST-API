from fastapi import Body, FastAPI , Response , status , HTTPException , Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title : str
    content : str
    published: bool
    id : int = 1

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='FastApi',user='postgres',password='kartik',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfully made")
        break
    except Exception as error:
        print("Connecting to server has some issues")
        print("Error : ", error)
        time.sleep(2)

@app.get("/")
async def root():
    return {"message": "World"}



@app.get("/sqlalchemy")
def test_posts(db : Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    print(posts)
    return {"data": "success"}



@app.get("/posts")
def post(db : Session = Depends(get_db)):
    # the common sql code used is in the 2 lines lower
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    return {"data": posts}



@app.post("/posts", status_code=status.HTTP_201_CREATED)# or to change the status code we can just pass another attribute next to posts as status_code=status.HTTP....
def create_post(post : Post, db : Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title , post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
# the things we actually require. -> title str, content str 



@app.get("/posts/{id}")
def indexPost(id: int , response: Response, db : Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""" , (str(id)))
    # indexed_post = cursor.fetchone()
    # print(indexed_post)
    indexed_post = db.query(models.Post).filter(models.Post.id == int(id)).first()
    
    if not indexed_post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id : {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} was not found")
    return {"post" : indexed_post}



@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()#very important line of code remember this
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} does not exist")
    else:
        db.delete(deleted_post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, post:Post, db : Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """ , (post.title , post.content , post.published , str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    posts = db.query(models.Post).filter(models.Post.id == id)
    updated_post = posts.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} does not exist")
    posts.update(post.dict())
    db.commit()
    return {"message": posts.first()}


# connection failed: Connection refused Is the server running on that host and accepting TCP/IP connections? connection to server at "localhost" (::1), port 5432 failed: Connection refused Is the server running on that host and accepting TCP/IP connections?
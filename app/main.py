from fastapi import Body, FastAPI , Response , status , HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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

@app.get("/posts")
def post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)# or to change the status code we can just pass another attribute next to posts as status_code=status.HTTP....
def create_post(post : Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title , post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}
# the things we actually require. -> title str, content str 

def findPost(id):
    for p in myposts:
        if p["id"] == id:
            return p

@app.get("/posts/{id}")
def indexPost(id: int , response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""" , (str(id)))
    indexed_post = cursor.fetchone()
    print(indexed_post)
    
    if not indexed_post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id : {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} was not found")
    return {"post" : indexed_post}

@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()#very important line of code remember this
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} does not exist")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """ , (post.title , post.content , post.published , str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} does not exist")
    return {"message": updated_post}

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str

@app.get("/")
async def root():
    return {"message": "World"}


@app.get("/posts")
def post():
    return {"data": "This is your post"}

@app.post("/createposts")
def creat_post(post : Post):
    print(post)
    return {"data": "post"}
# the things we actually require. -> title str, content str  
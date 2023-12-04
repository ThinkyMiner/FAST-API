from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "World"}


@app.get("/posts")
def post():
    return {"data": "This is your post"}

@app.post("/createposts")
def creat_post(payLoad: dict = Body(...)):
    print(payLoad)
    return {"new post": f"title : {payLoad['title']} :: Content : {payLoad['content']}"}
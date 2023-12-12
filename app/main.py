from fastapi import FastAPI
from .routers import user, posts, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['https://www.google.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "World"}
from fastapi import Body, FastAPI , Response , status , HTTPException , Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal,get_db
from typing import List
from . import utils
from .routers import user, posts, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='FastApi',user='postgres',password='kartik',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfully made")
#         break
#     except Exception as error:
#         print("Connecting to server has some issues")
#         print("Error : ", error)
#         time.sleep(2)

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "World"}
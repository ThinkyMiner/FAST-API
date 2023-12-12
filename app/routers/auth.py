from fastapi import  status , HTTPException , Depends, APIRouter
from app import utils
from . import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import  schemas, models
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user_in = db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user_in:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not utils.verifyPassword(user_credentials.password, user_in.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    access_token = oauth2.create_user_token(data={"user_id": user_in.id})
    return {"access_token": access_token, "token_type": "bearer_token"}


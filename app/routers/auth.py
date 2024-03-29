from fastapi import APIRouter, Depends, status , HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError
from .. import database, models, utils, schemas, oauth2
from typing import Type

router = APIRouter(
    
    tags=['Authentication']
    
)

@router.post('/login', response_model=schemas.LoginResponse)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    user:models.User or None = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    if utils.verify(user_credentials.password, user.password) is not True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Invalid credentials')
    token_data = {"id":user.id}
    access_token = oauth2.create_access_token(token_data)
    login_response = schemas.LoginResponse(
        id=user.id, 
        username=user.username, 
        email=user.email, 
        token = access_token, 
        token_type = "bearer")
    
    return login_response

@router.post('/get_current_user', response_model=schemas.UserCreated)
async def fetch_current_user(current_user :Type[models.User] | None= Depends(oauth2.get_current_user))->Type[models.User] | None:
    return current_user
from passlib.context import CryptContext
from fastapi import Header, HTTPException
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password:str)->str:
    return pwd_context.hash(password)

def verify(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_refresh_token(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    
    scheme, token = authorization.split()
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    
    return token
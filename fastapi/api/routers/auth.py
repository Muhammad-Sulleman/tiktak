from datetime import timedelta,timezone,datetime
from typing import Annotated
from fastapi import APIRouter ,Depends ,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt 
from dotenv import load_dotenv
from api.models import User
import os
from api.deps import db_dependency,user_dependency,brypt_context
load_dotenv()
router=APIRouter(
    prefix='/auth',
    tags=['auth']
)
SECRET_KEY=os.getenv('AUTH_SECRET_KEY')
ALGORITHM=os.getenv('AUTH_ALGORITHM')
print(f"SECRET_KEY: {SECRET_KEY}")
print(f"ALGORITHM: {ALGORITHM}")

#pydantic request for checking type of requests
class UserCreateRequest(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str
    
def AuthenticateUser(username:str,password:str,db):
    user=db.query(User).filter(User.username==username).first()
    if not user :
        return False
    if not brypt_context.verify(password,user.hashed_password):
        return False
    return user
 
        
def CreateAccessToken(username:str,userId:str,expires_delta:timedelta):
    encode= {
        'sub':username,'id':userId
    }
    expires=datetime.now(timezone.utc)+expires_delta
    encode.update(  {'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm='HS256')
@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request:UserCreateRequest):
    create_user_model=User(
       username=create_user_request.username,
       hashed_password=brypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()
@router.post('/token',response_model=Token)
async def login_for_access_token(formData:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user=AuthenticateUser(formData.username,formData.password,db)
    if not user :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token=CreateAccessToken(user.username,user.id,timedelta(minutes=20))
    return {'access_token':token,'token_type':'bearer'}


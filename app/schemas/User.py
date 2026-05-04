from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserInDB(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    role: Optional[str] = "client"

    phone:int
    address:str

    active:int

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    # rights:int
    
class UserOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    role: str
    phone:int
    address:str
    active:int
    created_at: datetime

class UserUpdate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password:str
    role: str
    phone:int
    address:str
    active:int
    updated_at: datetime
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class EmailRequest(BaseModel):
    email: EmailStr
    

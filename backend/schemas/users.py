from pydantic import BaseModel, EmailStr

class UserPublic(BaseModel):
    id : int
    email: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
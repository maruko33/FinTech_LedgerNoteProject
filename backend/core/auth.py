from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.deps import get_db, get_current_user
from core.security import hash_password, verify_password, create_access_token
from schemas.users import UserPublic,UserCreate
from schemas.auth import Token
from models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201, response_model= UserPublic)
async def register(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    email = payload.email
    password = payload.password

    result = await db.execute(select(User).where(User.email == email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")


    user = User(
        email=email,
        password_hash=hash_password(password),  
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": user.id, "email": user.email}

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):

    email = form_data.username
    password = form_data.password

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if not verify_password(password, user.password_hash):  
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)

@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}
from fastapi import APIRouter, HTTPException, Depends
from schemas.accounts import AccountCreate, AccountUpdate, AccountOut
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_db, get_current_user, pagination_params
from models.user import User
from crud.accounts import create_account,get_account,list_accounts,update_accounts

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/", response_model=AccountOut, status_code=201)
async def account_create(
    account_data: AccountCreate, 
    db:AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    return await create_account(db,current_user.id,account_data)


@router.get("/",response_model=list[AccountOut])
async def account_viewList(
    page: tuple[int, int] = Depends(pagination_params),
    db:AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    limit, offset = page
    return await list_accounts(db,current_user.id,limit,offset)

@router.get("/{id}", response_model=AccountOut)
async def account_viewID(
    id: int,
    db:AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_account(db,current_user.id, id)

@router.patch("/{id}", response_model=AccountOut)
async def modifyInfo(
    id:int,
    update_data:AccountUpdate,
    db:AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_accounts(id,update_data, db, current_user.id)
from models.ledger_account import LedgerAccount
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
async def create_account(db:AsyncSession, user_id:int, data):
    # 1) if parent_id is send：it has to be current user（or raise -> 404）
    if data.parent_id is not None:
        result = await db.execute(
            select(LedgerAccount).where(
                LedgerAccount.id == data.parent_id,
                LedgerAccount.user_id == user_id,
            )
        )
        parent = result.scalar_one_or_none()
        if parent is None:
            # use 404 becasue that won't release other account is exist
            raise HTTPException(status_code=404, detail="Account not found")
    
    account = LedgerAccount(
        user_id=user_id,
        name=data.name,
        type=data.type,
        subtype=data.subtype,
        currency=data.currency,
        parent_id=data.parent_id,
    )


    db.add(account)
    
    await db.flush()
    
    await db.refresh(account)
    return account


async def get_account(db,user_id,account_id):
    result = await db.execute(
        select(LedgerAccount).where(
            LedgerAccount.user_id == user_id,
            LedgerAccount.id == account_id
            )
    )
    account = result.scalar_one_or_none()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


async def list_accounts(db, user_id):
    result = await db.execute(
        select(LedgerAccount).where(
            LedgerAccount.user_id == user_id
            ).order_by(LedgerAccount.id.desc()).offset(0).limit(5)
    )
    accounts = result.scalars().all()
    return accounts


async def update_accounts(account_id:int,update_data,db,user_id:int):
    result = await db.execute(
        select(LedgerAccount).where(
            LedgerAccount.user_id == user_id,
            LedgerAccount.id == account_id
            )
    )
    account = result.scalar_one_or_none()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    if update_data.name is None and update_data.subtype is None and update_data.is_active is None:
        raise HTTPException(status_code=400, detail = "Bad Request")

    if update_data.name is not None:
        account.name = update_data.name
    if update_data.subtype is not None:
        account.subtype = update_data.subtype
    if update_data.is_active is not None:
        account.is_active = update_data.is_active
    
    await db.flush()
    
    await db.refresh(account)

    return account
    
    
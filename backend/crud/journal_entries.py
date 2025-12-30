from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from schemas.journal_entries import JournalEntryCreate
from models.journal_entry import JournalEntry
from models.posting import Posting
from fastapi import HTTPException
from models.ledger_account import LedgerAccount
from core.config import settings
async def create_journal_entry(journal_entry_data: JournalEntryCreate,db:AsyncSession,user_id:int):
    ###---Security Check Start---###
    #check number of postings >1
    if len(journal_entry_data.postings) < 2 :
        raise HTTPException(status_code=400, detail="At least 2 postings are required")    

    journal_entry =  JournalEntry(
        user_id = user_id,
        occurred_at = journal_entry_data.occurred_at,
        description = journal_entry_data.description,
    )
    
    
    db.add(journal_entry)
    await db.flush()

    total_minor = 0
    posts = []
    

    account_ids = {p.ledger_account_id for p in journal_entry_data.postings}
    result = await db.execute(
    select(LedgerAccount.id, LedgerAccount.is_active, LedgerAccount.currency)
        .where(
            LedgerAccount.user_id == user_id,
            LedgerAccount.id.in_(account_ids),
        )
    )
    rows = result.all()
    #check if posting account is belonging to user
    if(len(rows)!= len(account_ids)):
        raise HTTPException(status_code=404, detail="Account not Found")
    inactive_ids = [acc_id for acc_id, is_active, _ in rows if not is_active]
    #check if any posting account is inactive 
    if inactive_ids:
        raise HTTPException(status_code=400, detail=f"Inactive accounts: {inactive_ids}")
    account_currency = {acc_id: curr for acc_id, _, curr in rows}
        

    for post_data in journal_entry_data.postings:
        #check posting currency is same as account currency
        expected_currency = account_currency.get(post_data.ledger_account_id)
        if post_data.currency.upper() != expected_currency.upper():
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Currency mismatch for account {post_data.ledger_account_id}: "
                    f"expected {expected_currency}, got {post_data.currency}"
                ),
            )
        
        post = Posting(
            journal_entry_id = journal_entry.id,
            ledger_account_id = post_data.ledger_account_id,
            amount_minor = post_data.amount_minor,
            currency = post_data.currency,
            memo = post_data.memo,
        )

        posts.append(post)
        total_minor +=post_data.amount_minor
    if total_minor != 0:
        raise HTTPException(status_code=400,detail="Entry is not balanced")
    db.add_all(posts)
    await db.flush()
    result = await db.execute(
        select(JournalEntry)
        .options(selectinload(JournalEntry.postings))
        .where(JournalEntry.id == journal_entry.id, JournalEntry.user_id == user_id)
    )
    journal_entry_with_posts = result.scalar_one()
    return journal_entry_with_posts

async def list_journal_entries(db:AsyncSession, user_id:int, limit: int, offset:int):
    result = await db.execute(
        select(JournalEntry)
        .options(selectinload(JournalEntry.postings))
        .where(
            JournalEntry.user_id == user_id
        ).order_by(JournalEntry.id.desc()).offset(offset).limit(limit)
    )
    journals = result.scalars().all()
    return journals

async def get_journal_entries(journal_id: int, db:AsyncSession, user_id:int):
    result = await db.execute(
        select(JournalEntry)
        .options(selectinload(JournalEntry.postings))
        .where(
            JournalEntry.user_id == user_id,
            JournalEntry.id == journal_id
        )
    )
    journal = result.scalar_one_or_none()
    if journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    return journal


 
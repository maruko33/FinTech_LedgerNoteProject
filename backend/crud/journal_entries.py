from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from schemas.journal_entries import JournalEntryCreate,JournalEntryReversalIn,JournalEntryCorrectionIn
from models.journal_entry import JournalEntry
from models.posting import Posting
from fastapi import HTTPException
from models.ledger_account import LedgerAccount
from core.config import settings
from datetime import datetime, timezone
async def create_journal_entry(
        journal_entry_data: JournalEntryCreate,
        db:AsyncSession,
        user_id:int,
        *,
        correction_of_entry_id: int | None = None,
        reversal_of_entry_id: int | None = None,        
        ):
    ###---Security Check Start---###
    #check number of postings >1
    if len(journal_entry_data.postings) < 2 :
        raise HTTPException(status_code=400, detail="At least 2 postings are required")    

    journal_entry =  JournalEntry(
        user_id = user_id,
        occurred_at = journal_entry_data.occurred_at,
        description = journal_entry_data.description,
        correction_of_entry_id=correction_of_entry_id,
        reversal_of_entry_id=reversal_of_entry_id,
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

async def reverse_journal_entries(
    journal_id: int,
    journal_reversal_data: JournalEntryReversalIn | None,
    db: AsyncSession,
    user_id: int,
):
    # 1) check origin entry + postings
    stmt = (
        select(JournalEntry)
        .options(selectinload(JournalEntry.postings))
        .where(JournalEntry.user_id == user_id, JournalEntry.id == journal_id)
    )
    result = await db.execute(stmt)
    entry = result.scalar_one_or_none()
    if entry is None:
        raise HTTPException(status_code=404, detail="Journal entry not found")

    # 2) avoid repeatitive reversal（before create journal entry)
    already_reversed = await db.scalar(
        select(func.count())
        .select_from(JournalEntry)
        .where(
            JournalEntry.user_id == user_id,
            JournalEntry.reversal_of_entry_id == journal_id,
        )
    )
    if already_reversed and already_reversed > 0:
        raise HTTPException(status_code=400, detail="Entry already reversed")

    # defensive check
    if len(entry.postings) < 2:
        raise HTTPException(status_code=400, detail="Invalid entry: not enough postings")

    # create reversal entry（created after check, avoid dirty check)
    occurred_at = (
        journal_reversal_data.occurred_at
        if journal_reversal_data and journal_reversal_data.occurred_at
        else datetime.now(timezone.utc)
    )
    description = (
        journal_reversal_data.description
        if journal_reversal_data and journal_reversal_data.description
        else f"Reversal of entry {journal_id}"
    )

    journal_entry = JournalEntry(
        user_id=user_id,
        occurred_at=occurred_at,
        description=description,
        reversal_of_entry_id=journal_id,
    )
    db.add(journal_entry)
    await db.flush()  # 拿到 journal_entry.id

    # create reverse postings
    posts = [
        Posting(
            journal_entry_id=journal_entry.id,
            ledger_account_id=po.ledger_account_id,
            amount_minor=-po.amount_minor,
            currency=po.currency,
            memo=f"REVERSAL: {po.memo}" if po.memo else "REVERSAL",
        )
        for po in entry.postings
    ]
    db.add_all(posts)
    await db.flush()

    # check new entry of postings （avoid lazy-load serilization）
    result = await db.execute(
        select(JournalEntry)
        .options(selectinload(JournalEntry.postings))
        .where(JournalEntry.id == journal_entry.id, JournalEntry.user_id == user_id)
    )
    return result.scalar_one()


async def correct_journal_entries(
    journal_id: int,
    journal_correct_data: JournalEntryCorrectionIn,
    db: AsyncSession,
    user_id: int,
):
    occurred_at = (
        journal_correct_data.occurred_at
        if journal_correct_data and journal_correct_data.occurred_at
        else datetime.now(timezone.utc)
    )
    description = (
        journal_correct_data.description
        if journal_correct_data and journal_correct_data.description
        else f"Correction of entry {journal_id}"
    )
    corrected = journal_correct_data.corrected.model_copy(update={
        "occurred_at": occurred_at,
        "description": description,
    })
    return await create_journal_entry(corrected,db,user_id,correction_of_entry_id=journal_id)
 
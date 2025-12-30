from datetime import datetime
from sqlalchemy import select, func, case, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models.ledger_account import LedgerAccount
from models.posting import Posting
from models.journal_entry import JournalEntry
# from models.enums import EntryStatus  #uncomment if you only want to list the account that posted

async def trial_balance(db: AsyncSession, user_id: int, as_of: datetime):
    je_on = and_(
        JournalEntry.id == Posting.journal_entry_id,
        JournalEntry.user_id == user_id,
        JournalEntry.occurred_at <= as_of,
        # JournalEntry.status == EntryStatus.POSTED,  # Only count the posted account
    )

    amount_as_of = case(
        (JournalEntry.id.is_not(None), Posting.amount_minor),  
        else_=0,
    )

    stmt = (
        select(
            LedgerAccount.id.label("account_id"),
            LedgerAccount.name,
            LedgerAccount.type,
            LedgerAccount.currency,
            func.coalesce(func.sum(amount_as_of), 0).label("balance_minor"),
        )
        .select_from(LedgerAccount)
        .outerjoin(Posting, Posting.ledger_account_id == LedgerAccount.id)
        .outerjoin(JournalEntry, je_on)
        .where(LedgerAccount.user_id == user_id)
        .group_by(
            LedgerAccount.id,
            LedgerAccount.name,
            LedgerAccount.type,
            LedgerAccount.currency,
        )
        .order_by(LedgerAccount.type, LedgerAccount.name)
    )

    result = await db.execute(stmt)
    return result.mappings().all()

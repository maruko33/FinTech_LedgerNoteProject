from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db, get_current_user
from schemas.reports import TrialBalanceOut, TrialBalanceLine
from models.user import User
from crud.reports import trial_balance

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/trial-balance", response_model=TrialBalanceOut)
async def get_trial_balance(
    as_of: datetime | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    as_of_dt = as_of or datetime.now(timezone.utc)
    rows = await trial_balance(db, current_user.id, as_of_dt)

    lines = [
        TrialBalanceLine(
            account_id=r.account_id,
            name=r.name,
            type=r.type,
            currency=r.currency,
            balance_minor=int(r.balance_minor),
        )
        for r in rows
    ]
    return TrialBalanceOut(as_of=as_of_dt, lines=lines)
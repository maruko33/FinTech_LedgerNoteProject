from pydantic import BaseModel
from datetime import datetime
from models.enums import AccountType

class TrialBalanceLine(BaseModel):
    account_id: int
    name: str
    type: AccountType
    currency: str
    balance_minor: int

class TrialBalanceOut(BaseModel):
    as_of: datetime
    lines: list[TrialBalanceLine]

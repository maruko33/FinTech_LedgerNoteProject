from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

class PostingCreate(BaseModel):
    ledger_account_id:int
    amount_minor:int
    currency:str = Field(min_length=3,max_length=3)
    memo: str | None = None
    
    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, v: str) -> str:
        return v.upper()

class PostingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    journal_entry_id: int
    ledger_account_id: int
    amount_minor: int
    currency: str
    memo: str | None = None
    created_at: datetime
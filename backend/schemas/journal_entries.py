from pydantic import BaseModel,ConfigDict
from models.enums import EntrySource,EntryStatus
from datetime import datetime
from schemas.postings import PostingCreate, PostingOut

class JournalEntryCreate(BaseModel):
    occurred_at: datetime
    description: str
    postings: list[PostingCreate]

class JournalEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    user_id:int
    occurred_at:datetime
    description:str
    source:EntrySource
    status:EntryStatus
    correction_of_entry_id:int | None = None
    reversal_of_entry_id:int | None = None
    created_at: datetime
    postings: list[PostingOut] = []

class JournalEntryReversalIn(BaseModel):
    occurred_at: datetime | None = None
    description: str | None = None

class JournalEntryCorrectionIn(BaseModel):
    occurred_at: datetime | None = None
    description: str | None = None   
    corrected: JournalEntryCreate             

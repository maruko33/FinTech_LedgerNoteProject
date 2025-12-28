from pydantic import BaseModel, Field, field_validator, ConfigDict
from models.enums import AccountType
from datetime import datetime
class AccountCreate(BaseModel):
    name: str
    type: AccountType
    subtype: str | None = None
    currency: str = Field(min_length=3,max_length=3)
    parent_id: int | None = None
    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, v: str) -> str:
        return v.upper()
class AccountUpdate(BaseModel):
    name: str | None = None
    subtype: str | None = None
    is_active: bool | None = None

class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    type: AccountType
    subtype: str | None = None
    currency: str = Field(min_length=3, max_length=3)
    parent_id: int | None = None
    is_active: bool 
    created_at: datetime

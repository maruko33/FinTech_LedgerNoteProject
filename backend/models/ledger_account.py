from __future__ import annotations
from models.base import Base
from models.enums import AccountType
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

class LedgerAccount(Base):
    __tablename__ = "ledger_accounts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(80), nullable=False)
    type: Mapped[AccountType] = mapped_column(SAEnum(AccountType), nullable=False)
    subtype: Mapped[Optional[str]] = mapped_column(String(40))
    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ledger_accounts.id"))
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # relationships
    user: Mapped["User"] = relationship(back_populates="ledger_accounts")

    parent: Mapped[Optional["LedgerAccount"]] = relationship(
        remote_side="LedgerAccount.id",
        back_populates="children",
    )
    children: Mapped[List["LedgerAccount"]] = relationship(back_populates="parent")

    postings: Mapped[List["Posting"]] = relationship(back_populates="ledger_account")
    budget_lines: Mapped[List["BudgetLine"]] = relationship(back_populates="expense_account")

    __table_args__ = (
        Index("idx_la_user_type", "user_id", "type"),
        Index("idx_la_user_name", "user_id", "name"),
        UniqueConstraint("user_id", "name", name="uq_la_user_name"),
    )
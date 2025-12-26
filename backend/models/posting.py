from __future__ import annotations
from db.base import Base
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Posting(Base):
    __tablename__ = "postings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    journal_entry_id: Mapped[int] = mapped_column(ForeignKey("journal_entries.id"), nullable=False)
    ledger_account_id: Mapped[int] = mapped_column(ForeignKey("ledger_accounts.id"), nullable=False)

    amount_minor: Mapped[int] = mapped_column(BigInteger, nullable=False)  # +/- minor units
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    memo: Mapped[Optional[str]] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    journal_entry: Mapped["JournalEntry"] = relationship(back_populates="postings")
    ledger_account: Mapped["LedgerAccount"] = relationship(back_populates="postings")

    __table_args__ = (
        Index("idx_p_je", "journal_entry_id"),
        Index("idx_p_la_time", "ledger_account_id", "created_at"),
    )
from __future__ import annotations
from db.base import Base

from models.enums import EntrySource, EntryStatus
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship



class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    #time that this transaction happened
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    source: Mapped[EntrySource] = mapped_column(SAEnum(EntrySource), nullable=False, default=EntrySource.MANUAL)
    status: Mapped[EntryStatus] = mapped_column(SAEnum(EntryStatus), nullable=False, default=EntryStatus.POSTED)

    correction_of_entry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("journal_entries.id"))
    reversal_of_entry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("journal_entries.id"))
    #time that enroll this entry to notebook
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # relationships
    user: Mapped["User"] = relationship(back_populates="journal_entries")

    postings: Mapped[List["Posting"]] = relationship(back_populates="journal_entry", cascade="all, delete-orphan")

    correction_of: Mapped[Optional["JournalEntry"]] = relationship(
        foreign_keys=[correction_of_entry_id],
        remote_side="JournalEntry.id",
        back_populates="corrections",
    )
    corrections: Mapped[List["JournalEntry"]] = relationship(
        foreign_keys=[correction_of_entry_id],
        back_populates="correction_of",
    )

    reversal_of: Mapped[Optional["JournalEntry"]] = relationship(
        foreign_keys=[reversal_of_entry_id],
        remote_side="JournalEntry.id",
        back_populates="reversals",
    )
    reversals: Mapped[List["JournalEntry"]] = relationship(
        foreign_keys=[reversal_of_entry_id],
        back_populates="reversal_of",
    )

    __table_args__ = (
        Index("idx_je_user_time", "user_id", "occurred_at"),
        Index("idx_je_user_status", "user_id", "status"),
    )

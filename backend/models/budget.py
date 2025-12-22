from __future__ import annotations
from models.enums import BudgetPeriod
from models.base import Base
from datetime import datetime, date
from typing import List
from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(80), nullable=False)
    period: Mapped[BudgetPeriod] = mapped_column(SAEnum(BudgetPeriod), nullable=False, default=BudgetPeriod.MONTHLY)
    start_month: Mapped[date] = mapped_column(Date, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship(back_populates="budgets")
    lines: Mapped[List["BudgetLine"]] = relationship(back_populates="budget", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_b_user_month", "user_id", "start_month"),
    )

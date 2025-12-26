from __future__ import annotations
from db.base import Base
from datetime import datetime
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

class BudgetLine(Base):
    __tablename__ = "budget_lines"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    budget_id: Mapped[int] = mapped_column(ForeignKey("budgets.id"), nullable=False)

    expense_account_id: Mapped[int] = mapped_column(ForeignKey("ledger_accounts.id"), nullable=False)
    limit_minor: Mapped[int] = mapped_column(BigInteger, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    budget: Mapped["Budget"] = relationship(back_populates="lines")
    expense_account: Mapped["LedgerAccount"] = relationship(back_populates="budget_lines")

    __table_args__ = (
        UniqueConstraint("budget_id", "expense_account_id", name="uq_bl"),
    )
from sqlalchemy import Date, Numeric, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)

    date: Mapped[str] = mapped_column(Date)
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    payment_method: Mapped[str] = mapped_column(String(50))
    category_id: Mapped[int] = mapped_column(ForeignKey("expense_categories.id"))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    attachment_path: Mapped[str | None] = mapped_column(Text, nullable=True)

    category = relationship("ExpenseCategory")

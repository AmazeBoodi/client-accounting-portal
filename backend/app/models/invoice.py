from sqlalchemy import Date, Numeric, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), index=True)

    invoice_number: Mapped[str] = mapped_column(String(100))
    customer_name: Mapped[str] = mapped_column(String(255))
    issue_date: Mapped[str | None] = mapped_column(Date, nullable=True)
    due_date: Mapped[str] = mapped_column(Date)
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    payments = relationship("InvoicePayment", back_populates="invoice", cascade="all, delete-orphan")

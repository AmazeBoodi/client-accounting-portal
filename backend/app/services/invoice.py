from datetime import date as dt_date
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.models.invoice_payment import InvoicePayment
from app.models.invoice import Invoice

def invoice_totals(db: Session, invoice_id: int) -> tuple[float, float]:
    paid = db.scalar(select(func.coalesce(func.sum(InvoicePayment.amount), 0)).where(InvoicePayment.invoice_id == invoice_id))
    inv = db.get(Invoice, invoice_id)
    total = float(inv.total_amount)
    return float(paid), float(total)

def invoice_status(due_date: dt_date, paid: float, total: float) -> tuple[str, float, bool]:
    balance = round(total - paid, 2)
    if balance <= 0.00001:
        return "Paid", 0.0, False
    status = "Partially Paid" if paid > 0 else "Unpaid"
    is_overdue = (due_date < dt_date.today())
    return status, balance, is_overdue

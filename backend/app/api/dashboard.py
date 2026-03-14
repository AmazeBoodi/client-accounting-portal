from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from datetime import date

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.expense import Expense
from app.models.income import Income
from app.models.invoice import Invoice
from app.models.invoice_payment import InvoicePayment

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("")
def dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != "client" or not user.client_id:
        raise HTTPException(status_code=400, detail="Dashboard is client-only in MVP")
    cid = user.client_id

    # month range
    today = date.today()
    start_month = today.replace(day=1)

    income_month = db.scalar(select(func.coalesce(func.sum(Income.amount), 0)).where(Income.client_id == cid, Income.date >= start_month))
    expense_month = db.scalar(select(func.coalesce(func.sum(Expense.amount), 0)).where(Expense.client_id == cid, Expense.date >= start_month))

    # invoices outstanding
    invoices = db.scalars(select(Invoice).where(Invoice.client_id == cid)).all()
    outstanding = 0.0
    overdue = 0.0
    overdue_count = 0
    for inv in invoices:
        paid = db.scalar(select(func.coalesce(func.sum(InvoicePayment.amount), 0)).where(InvoicePayment.invoice_id == inv.id))
        balance = float(inv.total_amount) - float(paid or 0)
        if balance > 0.00001:
            outstanding += balance
            if inv.due_date < today:
                overdue += balance
                overdue_count += 1

    return {
        "month_income": float(income_month or 0),
        "month_expenses": float(expense_month or 0),
        "outstanding_invoices": round(outstanding, 2),
        "overdue_invoices_amount": round(overdue, 2),
        "overdue_invoices_count": overdue_count,
    }

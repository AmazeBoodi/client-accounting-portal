import io
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.expense import Expense
from app.models.income import Income
from app.models.invoice import Invoice
from app.models.invoice_payment import InvoicePayment

def to_csv_bytes(rows: list[dict]) -> bytes:
    df = pd.DataFrame(rows)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")

def export_expenses(db: Session, client_id: int | None):
    q = select(Expense)
    if client_id:
        q = q.where(Expense.client_id == client_id)
    items = db.scalars(q).all()
    rows = [{
        "id": e.id, "client_id": e.client_id, "date": e.date, "amount": float(e.amount),
        "payment_method": e.payment_method, "category_id": e.category_id, "notes": e.notes,
        "attachment_path": e.attachment_path
    } for e in items]
    return to_csv_bytes(rows)

def export_income(db: Session, client_id: int | None):
    q = select(Income)
    if client_id:
        q = q.where(Income.client_id == client_id)
    items = db.scalars(q).all()
    rows = [{
        "id": i.id, "client_id": i.client_id, "date": i.date, "amount": float(i.amount),
        "payment_method": i.payment_method, "category_id": i.category_id, "notes": i.notes,
        "attachment_path": i.attachment_path
    } for i in items]
    return to_csv_bytes(rows)

def export_invoices(db: Session, client_id: int | None):
    q = select(Invoice)
    if client_id:
        q = q.where(Invoice.client_id == client_id)
    items = db.scalars(q).all()
    rows = [{
        "id": inv.id, "client_id": inv.client_id, "invoice_number": inv.invoice_number, "customer_name": inv.customer_name,
        "issue_date": inv.issue_date, "due_date": inv.due_date, "total_amount": float(inv.total_amount), "notes": inv.notes
    } for inv in items]
    return to_csv_bytes(rows)

def export_invoice_payments(db: Session, client_id: int | None):
    q = select(InvoicePayment, Invoice).join(Invoice, InvoicePayment.invoice_id == Invoice.id)
    if client_id:
        q = q.where(Invoice.client_id == client_id)
    rows = []
    for pay, inv in db.execute(q).all():
        rows.append({
            "payment_id": pay.id,
            "invoice_id": inv.id,
            "client_id": inv.client_id,
            "invoice_number": inv.invoice_number,
            "payment_date": pay.payment_date,
            "amount": float(pay.amount),
            "payment_method": pay.payment_method,
            "notes": pay.notes
        })
    return to_csv_bytes(rows)

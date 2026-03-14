from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date

from app.api.deps import get_db, get_current_user, client_scope_filter
from app.models.invoice import Invoice
from app.models.invoice_payment import InvoicePayment
from app.models.user import User
from app.schemas.invoice import InvoiceCreate, InvoiceOut, InvoicePaymentCreate
from app.services.invoice import invoice_totals, invoice_status

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.get("", response_model=list[InvoiceOut])
def list_invoices(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    scope = client_scope_filter(user)
    q = select(Invoice).order_by(Invoice.due_date.asc())
    if scope:
        q = q.where(Invoice.client_id == scope)
    items = db.scalars(q).all()
    out = []
    for inv in items:
        paid, total = invoice_totals(db, inv.id)
        status, balance, overdue = invoice_status(inv.due_date, paid, total)
        out.append(InvoiceOut(
            id=inv.id, client_id=inv.client_id, invoice_number=inv.invoice_number, customer_name=inv.customer_name,
            issue_date=inv.issue_date, due_date=inv.due_date, total_amount=float(inv.total_amount), notes=inv.notes,
            paid_amount=paid, balance=balance, status=status, is_overdue=overdue
        ))
    return out

@router.post("", response_model=InvoiceOut)
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Admin should create invoices from client context (Phase 2).")
    inv = Invoice(
        client_id=user.client_id,
        invoice_number=payload.invoice_number,
        customer_name=payload.customer_name,
        issue_date=payload.issue_date,
        due_date=payload.due_date,
        total_amount=payload.total_amount,
        notes=payload.notes
    )
    db.add(inv); db.commit(); db.refresh(inv)
    paid, total = invoice_totals(db, inv.id)
    status, balance, overdue = invoice_status(inv.due_date, paid, total)
    return InvoiceOut(
        id=inv.id, client_id=inv.client_id, invoice_number=inv.invoice_number, customer_name=inv.customer_name,
        issue_date=inv.issue_date, due_date=inv.due_date, total_amount=float(inv.total_amount), notes=inv.notes,
        paid_amount=paid, balance=balance, status=status, is_overdue=overdue
    )

@router.post("/{invoice_id}/payments", response_model=InvoiceOut)
def add_payment(invoice_id: int, payload: InvoicePaymentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    inv = db.get(Invoice, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if user.role != "admin" and inv.client_id != user.client_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    pay = InvoicePayment(
        invoice_id=invoice_id,
        payment_date=payload.payment_date,
        amount=payload.amount,
        payment_method=payload.payment_method,
        notes=payload.notes
    )
    db.add(pay); db.commit()

    paid, total = invoice_totals(db, inv.id)
    status, balance, overdue = invoice_status(inv.due_date, paid, total)
    db.refresh(inv)
    return InvoiceOut(
        id=inv.id, client_id=inv.client_id, invoice_number=inv.invoice_number, customer_name=inv.customer_name,
        issue_date=inv.issue_date, due_date=inv.due_date, total_amount=float(inv.total_amount), notes=inv.notes,
        paid_amount=paid, balance=balance, status=status, is_overdue=overdue
    )

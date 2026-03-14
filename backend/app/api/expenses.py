import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date

from app.api.deps import get_db, get_current_user, client_scope_filter
from app.models.expense import Expense
from app.models.user import User
from app.core.config import settings
from app.schemas.expense import ExpenseCreate, ExpenseOut

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.get("", response_model=list[ExpenseOut])
def list_expenses(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    scope = client_scope_filter(user)
    q = select(Expense).order_by(Expense.date.desc())
    if scope:
        q = q.where(Expense.client_id == scope)
    return db.scalars(q).all()

@router.post("", response_model=ExpenseOut)
def create_expense(payload: ExpenseCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != "admin" and not user.client_id:
        raise HTTPException(status_code=400, detail="User has no client assigned")
    client_id = payload_client_id = (user.client_id if user.role == "client" else None)
    # Admin must pass client_id via header? Keep MVP: admin creates through client view in UI later.
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Admin should create expenses from client context (Phase 2).")
    e = Expense(
        client_id=client_id,
        date=payload.date,
        amount=payload.amount,
        payment_method=payload.payment_method,
        category_id=payload.category_id,
        notes=payload.notes,
    )
    db.add(e); db.commit(); db.refresh(e)
    return e

@router.post("/{expense_id}/attachment", response_model=ExpenseOut)
def upload_attachment(expense_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    e = db.get(Expense, expense_id)
    if not e:
        raise HTTPException(status_code=404, detail="Expense not found")
    if user.role != "admin" and e.client_id != user.client_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    # size check (best-effort)
    data = file.file.read()
    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    if len(data) > max_bytes:
        raise HTTPException(status_code=400, detail=f"File too large (max {settings.MAX_UPLOAD_MB} MB)")
    file.file.seek(0)

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    safe_name = f"expense_{expense_id}_{file.filename}".replace("/", "_")
    path = os.path.join(settings.UPLOAD_DIR, safe_name)
    with open(path, "wb") as f:
        f.write(data)
    e.attachment_path = safe_name
    db.add(e); db.commit(); db.refresh(e)
    return e

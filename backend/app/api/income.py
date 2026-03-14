import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db, get_current_user, client_scope_filter
from app.models.income import Income
from app.models.user import User
from app.core.config import settings
from app.schemas.income import IncomeCreate, IncomeOut

router = APIRouter(prefix="/income", tags=["income"])

@router.get("", response_model=list[IncomeOut])
def list_income(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    scope = client_scope_filter(user)
    q = select(Income).order_by(Income.date.desc())
    if scope:
        q = q.where(Income.client_id == scope)
    return db.scalars(q).all()

@router.post("", response_model=IncomeOut)
def create_income(payload: IncomeCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != "admin" and not user.client_id:
        raise HTTPException(status_code=400, detail="User has no client assigned")
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Admin should create income from client context (Phase 2).")
    i = Income(
        client_id=user.client_id,
        date=payload.date,
        amount=payload.amount,
        payment_method=payload.payment_method,
        category_id=payload.category_id,
        notes=payload.notes,
    )
    db.add(i); db.commit(); db.refresh(i)
    return i

@router.post("/{income_id}/attachment", response_model=IncomeOut)
def upload_attachment(income_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    i = db.get(Income, income_id)
    if not i:
        raise HTTPException(status_code=404, detail="Income not found")
    if user.role != "admin" and i.client_id != user.client_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    data = file.file.read()
    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    if len(data) > max_bytes:
        raise HTTPException(status_code=400, detail=f"File too large (max {settings.MAX_UPLOAD_MB} MB)")
    file.file.seek(0)

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    safe_name = f"income_{income_id}_{file.filename}".replace("/", "_")
    path = os.path.join(settings.UPLOAD_DIR, safe_name)
    with open(path, "wb") as f:
        f.write(data)
    i.attachment_path = safe_name
    db.add(i); db.commit(); db.refresh(i)
    return i

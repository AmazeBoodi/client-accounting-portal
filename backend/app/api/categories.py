from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db, get_current_user
from app.models.category import ExpenseCategory, IncomeCategory
from app.schemas.category import CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/expense", response_model=list[CategoryOut])
def expense_categories(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.scalars(select(ExpenseCategory).where(ExpenseCategory.is_active == True).order_by(ExpenseCategory.name)).all()

@router.get("/income", response_model=list[CategoryOut])
def income_categories(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.scalars(select(IncomeCategory).where(IncomeCategory.is_active == True).order_by(IncomeCategory.name)).all()

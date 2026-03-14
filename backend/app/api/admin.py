from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db, require_admin
from app.schemas.client import ClientCreate, ClientOut
from app.schemas.user import UserCreateClient, UserOut
from app.schemas.category import CategoryCreate, CategoryOut

from app.models.client import Client
from app.models.user import User
from app.models.category import ExpenseCategory, IncomeCategory
from app.core.security import hash_password

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/clients", response_model=ClientOut)
def create_client(payload: ClientCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    exists = db.scalar(select(Client).where(Client.name == payload.name))
    if exists:
        raise HTTPException(status_code=400, detail="Client name already exists")
    c = Client(name=payload.name)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("/clients", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.scalars(select(Client).order_by(Client.name)).all()

@router.post("/client-users", response_model=UserOut)
def create_client_user(payload: UserCreateClient, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status_code=400, detail="Email already exists")
    client = db.get(Client, payload.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    u = User(email=payload.email, name=payload.name, password_hash=hash_password(payload.password), role="client", client_id=payload.client_id)
    db.add(u); db.commit(); db.refresh(u)
    return u

@router.post("/expense-categories", response_model=CategoryOut)
def create_expense_category(payload: CategoryCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if db.scalar(select(ExpenseCategory).where(ExpenseCategory.name == payload.name)):
        raise HTTPException(status_code=400, detail="Category exists")
    c = ExpenseCategory(name=payload.name, is_active=payload.is_active)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("/expense-categories", response_model=list[CategoryOut])
def list_expense_categories(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.scalars(select(ExpenseCategory).order_by(ExpenseCategory.name)).all()

@router.post("/income-categories", response_model=CategoryOut)
def create_income_category(payload: CategoryCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if db.scalar(select(IncomeCategory).where(IncomeCategory.name == payload.name)):
        raise HTTPException(status_code=400, detail="Category exists")
    c = IncomeCategory(name=payload.name, is_active=payload.is_active)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("/income-categories", response_model=list[CategoryOut])
def list_income_categories(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.scalars(select(IncomeCategory).order_by(IncomeCategory.name)).all()

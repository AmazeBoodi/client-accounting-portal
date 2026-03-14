from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, client_scope_filter
from app.models.user import User
from app.services.export import export_expenses, export_income, export_invoices, export_invoice_payments

router = APIRouter(prefix="/exports", tags=["exports"])

@router.get("/expenses.csv")
def expenses_csv(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    scope = client_scope_filter(user)
    data = export_expenses(db, scope)
    return Response(content=data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=expenses.csv"})

@router.get("/income.csv")
def income_csv(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    scope = client_scope_filter(user)
    data = export_income(db, scope)
    return Response(content=data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=income.csv"})

@router.get("/invoices.csv")
def invoices_csv(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    scope = client_scope_filter(user)
    data = export_invoices(db, scope)
    return Response(content=data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=invoices.csv"})

@router.get("/invoice_payments.csv")
def invoice_payments_csv(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    scope = client_scope_filter(user)
    data = export_invoice_payments(db, scope)
    return Response(content=data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=invoice_payments.csv"})

from pydantic import BaseModel
from datetime import date

class InvoiceCreate(BaseModel):
    invoice_number: str
    customer_name: str
    issue_date: date | None = None
    due_date: date
    total_amount: float
    notes: str | None = None

class InvoicePaymentCreate(BaseModel):
    payment_date: date
    amount: float
    payment_method: str
    notes: str | None = None

class InvoiceOut(BaseModel):
    id: int
    client_id: int
    invoice_number: str
    customer_name: str
    issue_date: date | None
    due_date: date
    total_amount: float
    notes: str | None

    paid_amount: float
    balance: float
    status: str
    is_overdue: bool

    class Config:
        from_attributes = True

from pydantic import BaseModel
from datetime import date

class ExpenseCreate(BaseModel):
    date: date
    amount: float
    payment_method: str
    category_id: int
    notes: str | None = None

class ExpenseOut(BaseModel):
    id: int
    client_id: int
    date: date
    amount: float
    payment_method: str
    category_id: int
    notes: str | None
    attachment_path: str | None

    class Config:
        from_attributes = True

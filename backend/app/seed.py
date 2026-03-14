import os
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.user import User
from app.models.client import Client
from app.models.category import ExpenseCategory, IncomeCategory
from app.core.security import hash_password

def run():
    db: Session = SessionLocal()
    try:
        # Admin user
        admin_email = os.getenv("ADMIN_EMAIL", "admin@portal.com")
        admin_pass = os.getenv("ADMIN_PASSWORD", "admin12345")
        if not db.scalar(select(User).where(User.email == admin_email)):
            admin = User(email=admin_email, name="Admin", password_hash=hash_password(admin_pass), role="admin", is_active=True)
            db.add(admin)
            db.commit()

        # Default categories
        defaults_exp = ["Rent", "Utilities", "Marketing", "Office Supplies", "Transport", "Meals"]
        for name in defaults_exp:
            if not db.scalar(select(ExpenseCategory).where(ExpenseCategory.name == name)):
                db.add(ExpenseCategory(name=name, is_active=True))
        defaults_inc = ["Sales", "Services", "Other Income"]
        for name in defaults_inc:
            if not db.scalar(select(IncomeCategory).where(IncomeCategory.name == name)):
                db.add(IncomeCategory(name=name, is_active=True))
        db.commit()
        print("Seed completed. Admin:", admin_email, "Password:", admin_pass)
    finally:
        db.close()

if __name__ == "__main__":
    run()

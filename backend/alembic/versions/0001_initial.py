"""initial

Revision ID: 0001_initial
Revises:
Create Date: 2026-01-17
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False, server_default="client"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("client_id", sa.Integer(), sa.ForeignKey("clients.id"), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "expense_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "income_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("client_id", sa.Integer(), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(12,2), nullable=False),
        sa.Column("payment_method", sa.String(length=50), nullable=False),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("expense_categories.id"), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("attachment_path", sa.Text(), nullable=True),
    )
    op.create_index("ix_expenses_client_id", "expenses", ["client_id"])

    op.create_table(
        "income",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("client_id", sa.Integer(), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(12,2), nullable=False),
        sa.Column("payment_method", sa.String(length=50), nullable=False),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("income_categories.id"), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("attachment_path", sa.Text(), nullable=True),
    )
    op.create_index("ix_income_client_id", "income", ["client_id"])

    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("client_id", sa.Integer(), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("invoice_number", sa.String(length=100), nullable=False),
        sa.Column("customer_name", sa.String(length=255), nullable=False),
        sa.Column("issue_date", sa.Date(), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("total_amount", sa.Numeric(12,2), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
    )
    op.create_index("ix_invoices_client_id", "invoices", ["client_id"])

    op.create_table(
        "invoice_payments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("invoice_id", sa.Integer(), sa.ForeignKey("invoices.id"), nullable=False),
        sa.Column("payment_date", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(12,2), nullable=False),
        sa.Column("payment_method", sa.String(length=50), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
    )
    op.create_index("ix_invoice_payments_invoice_id", "invoice_payments", ["invoice_id"])

def downgrade():
    op.drop_index("ix_invoice_payments_invoice_id", table_name="invoice_payments")
    op.drop_table("invoice_payments")
    op.drop_index("ix_invoices_client_id", table_name="invoices")
    op.drop_table("invoices")
    op.drop_index("ix_income_client_id", table_name="income")
    op.drop_table("income")
    op.drop_index("ix_expenses_client_id", table_name="expenses")
    op.drop_table("expenses")
    op.drop_table("income_categories")
    op.drop_table("expense_categories")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_table("clients")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.admin import router as admin_router
from app.api.categories import router as categories_router
from app.api.expenses import router as expenses_router
from app.api.income import router as income_router
from app.api.invoices import router as invoices_router
from app.api.dashboard import router as dashboard_router
from app.api.exports import router as exports_router

app = FastAPI(title="Client Accounting Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(categories_router)
app.include_router(expenses_router)
app.include_router(income_router)
app.include_router(invoices_router)
app.include_router(dashboard_router)
app.include_router(exports_router)

@app.get("/health")
def health():
    return {"ok": True}

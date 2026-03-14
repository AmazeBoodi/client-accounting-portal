from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="client")  # admin/client
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    client_id: Mapped[int | None] = mapped_column(ForeignKey("clients.id"), nullable=True)
    client = relationship("Client", back_populates="users")

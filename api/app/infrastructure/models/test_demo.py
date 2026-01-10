import uuid
from datetime import datetime
from sqlalchemy import  String, PrimaryKeyConstraint, UUID, TEXT, TIMESTAMP, text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class DemoModel(Base):
    """测试下alembic"""
    __tablename__ = "demos"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_demos_id"),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("''::character varying"))
    age: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    description: Mapped[str] = mapped_column(TEXT, nullable=False, server_default=text("''::text"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
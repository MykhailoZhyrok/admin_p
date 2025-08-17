from datetime import datetime
from typing import Optional
from uuid import uuid4
import enum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base.base_prod import BaseProd
from app.models.product import ProductsOrm


class OrderStatus(str, enum.Enum):
    pending = "pending"       
    paid = "paid"           
    shipped = "shipped"   
    completed = "completed" 
    canceled = "canceled"     


class OrderOrm(BaseProd):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True, index=True)

    user_id: Mapped[Optional[int]] = mapped_column(nullable=True, index=True)

    session_token: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)

    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subtotal: Mapped[float] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(3), default="PLN")

    items: Mapped[list["OrderItemOrm"]] = relationship(
        "OrderItemOrm",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class OrderItemOrm(BaseProd):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2))

    order: Mapped["OrderOrm"] = relationship("OrderOrm", back_populates="items")
    product: Mapped["ProductsOrm"] = relationship("ProductsOrm", lazy="joined")

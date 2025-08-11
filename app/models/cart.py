from datetime import datetime
import enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime, Enum, Integer, Numeric, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base.base_cart import BaseCart
from app.models.product import ProductsOrm


class CartStatus(str, enum.Enum):
    draft = "draft"
    converted = "converted" 

class CartOrm(BaseCart):
    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(nullable=True, index=True)
    session_token: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)  # для гостей
    status: Mapped[CartStatus] = mapped_column(Enum(CartStatus), default=CartStatus.draft, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    items: Mapped[list["CartItemOrm"]] = relationship(
        "CartItemOrm",
        back_populates="cart",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    subtotal: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="PLN")

class CartItemOrm(BaseCart):
    __tablename__ = "cart_items"
    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cartitem_cart_product"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2))

    cart: Mapped["CartOrm"] = relationship("CartOrm", back_populates="items")
    product: Mapped["ProductsOrm"] = relationship("ProductsOrm", lazy="joined")



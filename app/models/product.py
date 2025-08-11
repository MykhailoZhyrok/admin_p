from typing import Optional

from sqlalchemy import Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base.base_prod import BaseProd
from app.models.category import CategoriesOrm


class ProductsOrm(BaseProd):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2))
    is_active: Mapped[bool] = mapped_column(default=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    category: Mapped["CategoriesOrm"] = relationship(
        "CategoriesOrm", back_populates="products"
    )

from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base.base_prod import BaseProd

if TYPE_CHECKING:
    from app.models.product import ProductsOrm


class CategoriesOrm(BaseProd):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(200))

    products: Mapped[List["ProductsOrm"]] = relationship(
        "ProductsOrm", back_populates="category"
    )

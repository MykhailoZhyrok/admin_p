from datetime import datetime
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated, Optional


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    price: Annotated[Decimal, Field(max_digits=12, decimal_places=2)]
    is_active: bool = True
    stock_quantity: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Annotated[Decimal, Field(max_digits=12, decimal_places=2)]
    is_active: Optional[bool] = None
    stock_quantity: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    image_path: Optional[str] = None 
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
        from_attributes = True

class ProductData(BaseModel):
    name: str
    category_id: int
    price: Decimal
    is_active: bool
    stock_quantity: int
    description: Optional[str] = None
    image_path: Optional[str] = None

class ProductFormData(BaseModel):
    name: str
    description: str | None
    category_id: int
    price: float
    is_active: bool
    stock_quantity: int
    file: UploadFile

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str | None = Form(None),
        category_id: int = Form(...),
        price: float = Form(...),
        is_active: bool = Form(True),
        stock_quantity: int = Form(0),
        file: UploadFile = File(...)
    ):
        return cls(
            name=name,
            description=description,
            category_id=category_id,
            price=price,
            is_active=is_active,
            stock_quantity=stock_quantity,
            file=file
        )
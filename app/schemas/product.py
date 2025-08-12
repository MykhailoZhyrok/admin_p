from datetime import datetime
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

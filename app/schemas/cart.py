from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from app.schemas.product import ProductResponse


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    product: Optional[ProductResponse]
    class Config:
        orm_mode = True
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    public_id: str
    user_id: Optional[int]
    session_token: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    subtotal: Optional[Decimal]
    currency: str
    items: List[CartItemResponse]

    class Config:
        orm_mode = True
        from_attributes = True

class ChangeCartVal(BaseModel):
    product_id: int
    user_id: Optional[int] = None  
    session_token: Optional[str] = None  

class AddToCartRequest(ChangeCartVal):
    quantity: int = 1

class UpdatedQuantityCart(ChangeCartVal):
    add_quantity: int = 1




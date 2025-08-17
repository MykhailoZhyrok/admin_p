from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

from app.schemas.product import ProductResponse


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    completed = "completed"
    cancelled = "cancelled"

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    product: Optional[ProductResponse]
    class Config:
        orm_mode = True
        from_attributes = True

class OrderBase(BaseModel):
    user_id: Optional[int] = Field(None, description="ID пользователя, если авторизован")
    session_token: Optional[str] = Field(None, description="Сессия для гостевого заказа")
    subtotal: float = Field(..., gt=0, description="Общая сумма заказа")
    currency: str = Field("PLN", min_length=3, max_length=3, description="Валюта заказа")
    status: OrderStatus = Field(OrderStatus.pending, description="Статус заказа")
    shipping_address: Optional[str] = Field(None, description="Адрес доставки")
    billing_address: Optional[str] = Field(None, description="Адрес оплаты")
    items: List[OrderItemResponse]
        


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    public_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class AddToOrderRequest(BaseModel):
    user_id: Optional[int] = Field(None, description="ID пользователя, если авторизован")
    session_token: Optional[str] = Field(None, description="Сессия для гостевого заказа")
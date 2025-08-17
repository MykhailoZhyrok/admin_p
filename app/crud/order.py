from decimal import Decimal
from typing import Dict, Optional

from pathlib import Path
from uuid import uuid4 
from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload, selectinload
from app.models.cart import CartItemOrm, CartOrm
from app.models.order import OrderItemOrm, OrderOrm, OrderStatus
from app.models.product import ProductsOrm
from app.schemas.cart import CartItemResponse, CartResponse
from app.schemas.order import OrderBase, OrderItemResponse, OrderRead
from app.schemas.product import ProductData, ProductResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


class OrderService:
    @staticmethod
    async def get_all_orders(session: AsyncSession) -> list[OrderRead]:
        result = await session.execute(select(OrderOrm))

        if not result:
            raise HTTPException(status_code=400, detail="Orders not found")
        return result.scalars().all() 
    
    @staticmethod
    async def add_cart_to_order(session: AsyncSession, user_id: int | None = None, session_token: str | None = None)->OrderRead:

        stmt = select(CartOrm).where(
            (CartOrm.user_id == user_id) if user_id else (CartOrm.session_token == session_token)
        )
        result = await session.execute(stmt)
        cart = result.scalar_one_or_none()
        
        if not cart:
            raise HTTPException(status_code=400, detail="Cart not found")
        if len(cart.items) == 0:
            raise HTTPException(status_code=400, detail="It is empty cart")
        
        order = OrderOrm(
            user_id=cart.user_id,
            session_token=cart.session_token,
            subtotal=cart.subtotal or 0,
            currency=cart.currency,
            status=OrderStatus.pending
        )
        
        order.items = [
            OrderItemOrm(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
            for item in cart.items
            
        ]

        session.add(order)
        await session.delete(cart) 
        await session.commit()
        await session.refresh(order)

        return order


    @staticmethod
    async def get_user_order(session: AsyncSession, public_id: str ) ->list[OrderRead]:
        if not public_id:
            raise HTTPException(status_code=400, detail="Invalid order public_id")
        stmt = select(OrderOrm).where(
            OrderOrm.public_id == public_id
        )
        result = await session.execute(stmt)

        if not result:
            raise HTTPException(status_code=404, detail="Orders not found")
        return result.scalars().all()
    
    @staticmethod
    async def change_order_status(session: AsyncSession, order_id: int, new_status: OrderStatus) ->OrderRead:
        stmt = update(OrderOrm).where(OrderOrm.id == order_id).values(status=new_status).returning(OrderOrm)
        result = await session.execute(stmt)
        updated_order = result.scalar_one_or_none()
        
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        await session.commit()
        await session.refresh(updated_order)
        
        return updated_order


        
         
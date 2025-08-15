from decimal import Decimal
from typing import Dict, Optional

from pathlib import Path
from uuid import uuid4 
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from app.models.cart import CartItemOrm, CartOrm
from app.models.product import ProductsOrm
from app.schemas.cart import CartItemResponse, CartResponse
from app.schemas.product import ProductData, ProductResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


class CartService:
    @staticmethod
    async def get_all_carts(session: AsyncSession) -> list[CartResponse]:
        result = await session.execute(select(CartOrm))
        carts = result.scalars().all()
        return [CartResponse.from_orm(cart) for cart in carts]
    
    @staticmethod
    async def add_to_cart(session: AsyncSession, product_id: int, get_quantity: int, user_id: int | None = None, session_token: str | None = None)->CartResponse:

        if get_quantity > 0:
            raise HTTPException(status_code=404, detail="Quantity can not be zero")
        
        product = await session.get(ProductsOrm, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        if product.stock_quantity < get_quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")

        # 2. Ищем корзину пользователя или по токену сессии
        stmt = select(CartOrm).where(
            (CartOrm.user_id == user_id) if user_id else (CartOrm.session_token == session_token)
        )
        result = await session.execute(stmt)
        cart = result.scalar_one_or_none()

        # 3. Если корзины нет — создаём
        if not cart:
            cart = CartOrm(
                user_id=user_id,
                session_token=session_token or str(uuid4())
            )
            session.add(cart)
            await session.flush()  # чтобы получить cart.id

        # 4. Проверяем, есть ли этот товар в корзине
        stmt = select(CartItemOrm).where(
            CartItemOrm.cart_id == cart.id,
            CartItemOrm.product_id == product.id
        )
        result = await session.execute(stmt)
        cart_item = result.scalar_one_or_none()

        if cart_item:
            # обновляем количество
            cart_item.quantity += get_quantity
        else:
            # добавляем новый товар
            cart_item = CartItemOrm(
                cart_id=cart.id,
                product_id=product.id,
                quantity=get_quantity,
                unit_price=Decimal(product.price)
            )
            session.add(cart_item)
        product.stock_quantity -= get_quantity
        if product.stock_quantity < 0:
            raise HTTPException(status_code=400, detail="Stock went below zero (possible race condition)")

        # 5. Пересчитываем subtotal
        stmt = select(CartItemOrm).where(CartItemOrm.cart_id == cart.id)
        result = await session.execute(stmt)
        items = result.scalars().all()
        cart.subtotal = sum(item.unit_price * item.quantity for item in items)

        await session.commit()
        await session.refresh(cart)

        return cart
    
    @staticmethod
    async def change_quantity(session: AsyncSession, product_id: int, add_quantity: int, user_id: int | None = None, session_token: str | None = None)->CartResponse:
        if add_quantity == 0:
            raise HTTPException(status_code=400, detail="Quantity can not be zero")
        product = await session.get(ProductsOrm, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        if product.stock_quantity < add_quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")
        
        # 2. Ищем корзину пользователя или по токену сессии
        stmt = select(CartOrm).where(
            (CartOrm.user_id == user_id) if user_id else (CartOrm.session_token == session_token)
        )
        result = await session.execute(stmt)
        cart = result.scalar_one_or_none()

        # 3. Если корзины нет — создаём
        if not cart:
            raise HTTPException(status_code=400, detail="Cart not found")
        
        stmt = select(CartItemOrm).where(
            CartItemOrm.cart_id == cart.id,
            CartItemOrm.product_id == product.id
        )
        result = await session.execute(stmt)
        cart_item = result.scalar_one_or_none()

        if cart_item:
            cart_item.quantity += add_quantity
        else:
            raise HTTPException(status_code=400, detail="Product not found in cart")
        product.stock_quantity -= add_quantity
        if product.stock_quantity <=0:
            session.delete(cart_item)
        if product.stock_quantity < 0:
            raise HTTPException(status_code=400, detail="Stock went below zero (possible race condition)")
        
        stmt = select(CartItemOrm).where(CartItemOrm.cart_id == cart.id)
        result = await session.execute(stmt)
        items = result.scalars().all()
        cart.subtotal = sum(item.unit_price * item.quantity for item in items)

        await session.commit()
        await session.refresh(cart)

        return cart
    
    @staticmethod
    async def get_user_cart(session: AsyncSession, public_id: str ) ->list[CartItemResponse]:
        if not public_id:
            raise HTTPException(status_code=400, detail="Invalid cart id")
        stmt = select(CartOrm).where(
            CartOrm.public_id == public_id
        )
        result = await session.execute(stmt)
        cart = result.scalar_one_or_none()

        if not cart:
            raise HTTPException(status_code=400, detail="Cart not found")
        return cart.items

    @staticmethod
    async def remove_item(session: AsyncSession,  product_id: int, user_id: int | None = None, session_token: str | None = None) ->CartResponse:
        
 
        stmt = select(CartOrm).where(
            (CartOrm.user_id == user_id) if user_id else (CartOrm.session_token == session_token)
        )
        result = await session.execute(stmt)
        cart = result.scalar_one_or_none()

        # 3. Если корзины нет — создаём
        if not cart:
            raise HTTPException(status_code=400, detail="Cart not found")
        
        stmt = select(CartItemOrm).where(
            CartItemOrm.cart_id == cart.id,
            CartItemOrm.product_id == product_id
        )
        result = await session.execute(stmt)
        cart_item = result.scalar_one_or_none()

        if not cart_item:
            raise HTTPException(status_code=400, detail="Product not found in cart")

        await session.delete(cart_item)  

        # Пересчитываем subtotal
        stmt = select(CartItemOrm).where(CartItemOrm.cart_id == cart.id)
        result = await session.execute(stmt)
        items = result.scalars().all()
        cart.subtotal = sum(item.unit_price * item.quantity for item in items)

        # Коммитим всё одним разом
        await session.commit()
        await session.refresh(cart)


        return cart
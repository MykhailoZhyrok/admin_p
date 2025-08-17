from typing import List
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.order import OrderService
from app.db.session import get_prod_session
from app.models.order import OrderStatus
from app.schemas.order import AddToOrderRequest, OrderBase, OrderItemResponse, OrderRead 

order_router = APIRouter()


@order_router.post(
    "/order/add",
    summary="Створити завмовлення",
    description="Перенести кошик до завмовлень",
    response_model=OrderRead,
    tags=["Замовлення"]
)
async def add_to_order(
    data: AddToOrderRequest,
    session: AsyncSession = Depends(get_prod_session)
):
    try:
        order = await OrderService.add_cart_to_order(
            session=session,
            user_id=data.user_id,
            session_token=data.session_token,
        
        )
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@order_router.get("/orders", 
                    summary="Отримати всі замовлення",
                    description="Повертає список усіх наявних замовлень у базі.",
                    response_model=List[OrderRead], tags=["Замовлення"])
async def get_orders(session: AsyncSession = Depends(get_prod_session)):
        try:
            return await OrderService.get_all_orders(session=session)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
        
@order_router.get("/orders/{public_id}", 
                    summary="Отримати замовлення користувача",
                    description="Повертає список усіх наявних замовлень замовлень користувача",
                    response_model=List[OrderRead], tags=["Замовлення"])
async def get_user_orders(public_id: str, session: AsyncSession = Depends(get_prod_session), ):
        try:
            return await OrderService.get_user_order(session=session, public_id=public_id)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@order_router.patch(
    "/order/status/{order_id}",
    summary="Изменить статус заказа",
    description="меняет статус заказа ",
    response_model=OrderRead,
    tags=["Замовлення"]
)
async def updated_quantity(
    order_id: int,
    new_status: OrderStatus = Query(..., description="Новый статус заказа"),
    session: AsyncSession = Depends(get_prod_session)
):
    try:
        return await OrderService.change_order_status(session=session, order_id=order_id, new_status = new_status)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    
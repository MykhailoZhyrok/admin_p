from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.cart import CartService
from app.schemas.cart import AddToCartRequest, CartItemResponse, CartResponse, UpdatedQuantityCart
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.db.session import get_prod_session 

cart_router = APIRouter()


@cart_router.post(
    "/carts/add",
    summary="Додати товар до кошика",
    description="Створює або оновлює кошик користувача / гостя",
    response_model=CartResponse,
    tags=["Кошик"]
)
async def add_to_cart(
    data: AddToCartRequest,
    session: AsyncSession = Depends(get_prod_session)
):
    try:
        cart = await CartService.add_to_cart(
            session=session,
            product_id=data.product_id,
            get_quantity=data.quantity,
            user_id=data.user_id,
            session_token=data.session_token
        )
        return cart
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@cart_router.get("/carts", 
                    summary="Отримати всі кошики",
                    description="Повертає список усіх наявних кошиків у базі.",
                    response_model=List[CartResponse], tags=["Кошик"])
async def get_carts(session: AsyncSession = Depends(get_prod_session)):
        try:
            result = await CartService.get_all_carts(session=session)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@cart_router.patch(
    "/cart/items/",
    summary="Изменить количество товара",
    description="Увеличивает количество на +n товара в кошику користувача / гостя",
    response_model=CartResponse,
    tags=["Кошик"]
)
async def updated_quantity(
    data: UpdatedQuantityCart,
    session: AsyncSession = Depends(get_prod_session)
):
    try:
        cart = await CartService.change_quantity(
            session=session,
            product_id=data.product_id,
            add_quantity=data.add_quantity,
            user_id=data.user_id,
            session_token=data.session_token
        )
        return cart
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    
@cart_router.get("/carts/{public_id}", 
                    summary="Отримати кошик користувача",
                    description="Повертає список товарів в кошику користувача",
                    response_model=List[CartItemResponse], tags=["Кошик"])
async def get_user_cart(
    public_id: str,
    session: AsyncSession = Depends(get_prod_session)
):
        try:
            result = await CartService.get_user_cart(
                session=session,
                public_id = public_id
                )
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
        

@cart_router.delete(
    "/cart/{product_id}",
    summary="Удалить товар из корзины",
    description="Удаляет товар по его ID из корзины пользователя или гостевой корзины (по session_token).",
    tags=["Кошик"],
    response_model=CartResponse
)
async def delete_product_from_cart(
    product_id: int,
    user_id: int | None = None,
    session_token: str | None = None,
    session: AsyncSession = Depends(get_prod_session)
):
    try:
        return await CartService.remove_item(
            session=session,
            product_id=product_id,
            user_id=user_id,
            session_token=session_token
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

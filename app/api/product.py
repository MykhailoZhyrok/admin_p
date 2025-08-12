from decimal import Decimal
from typing import Annotated, List, Optional
from fastapi import File, Form, UploadFile, APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.crud.product import ProductsService
from app.db.session import get_prod_session
from app.models.user import UsersOrm
from app.crud.user import UserService
from app.utils.uploader import uploaderImg

get_current_user = UserService.get_current_user

product_router = APIRouter()



@product_router.get(
    "/products",
    summary="Отримати всі продукти",
    description="Повертає список усіх продуктів у базі.",
    response_model=List[ProductResponse],
    tags=["Продукт"]
)
async def get_products(session: AsyncSession = Depends(get_prod_session)):
    try:
        return await ProductsService.get_all_products(session=session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@product_router.post(
    "/product",
    summary="Створити новий продукт",
    description="Додає новий продукт з назвою, описом і категорією. Вимагає авторизацію.",
    tags=["Продукт"]
)
async def insert_product_api(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    category_id: int = Form(...),
    price: Decimal = Form(...),
    is_active: bool = Form(True),
    stock_quantity: int = Form(0),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_prod_session),
    _: UsersOrm = Depends(get_current_user)
):
    try:
        image_path = await uploaderImg(file)
        new_product = await ProductsService.insert_product(
            session=session,
            name=name,
            description = description,
            category_id=category_id,
            price=price,
            is_active=is_active,
            stock_quantity=stock_quantity,
            image_path=image_path
        )
        return new_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@product_router.delete(
    "/product/{product_id}",
    summary="Видалити продукт",
    description="Видаляє продукт за ID, якщо такий існує.",
    tags=["Продукт"]
)
async def delete_prodct_by_id_api(
    product_id: int,
    session: AsyncSession = Depends(get_prod_session)
):
    try:
        success = await ProductsService.delete_product_by_id(product_id, session=session)
        return {"message": f"Product was deleted, {success}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@product_router.put(
    "/products/{product_id}",
    summary="Оновити продукт",
    description="Оновлює продукт за його ID. Можна змінити назву, опис і категорію.",
    tags=["Продукт"]
)
async def update_product(
    product_id: int,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    category_id: int = Form(...),
    price: Decimal = Form(...),
    is_active: bool = Form(True),
    stock_quantity: int = Form(0),
    file: Optional[UploadFile] = File(None),
    session: AsyncSession = Depends(get_prod_session),
    # _: UsersOrm = Depends(get_current_user)
):
    image_path = await uploaderImg(file)
    updated = await ProductsService.update_product_by_id(
        session=session,
        product_id=product_id,
        name=name,
        description=description,
        category_id=category_id,
        price=price,
        is_active=is_active,
        stock_quantity=stock_quantity,
        image_path=image_path
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@product_router.get(
    "/products/{product_id}",
    summary="Отримати продукт за ID",
    description="Повертає інформацію про один продукт за його ID. Якщо не знайдено — 404.",
    tags=["Продукт"]
)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_prod_session)
):
    product = await ProductsService.get_product_by_id(product_id, session=session)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

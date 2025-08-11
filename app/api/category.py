from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.crud.category import CategoryService  
from app.db.session import get_prod_session 

category_router = APIRouter()


@category_router.get("/")
def read_root():
        return {"Hello": "World"}


@category_router.post("/category",summary="Створити категорію",
    description="Додає нову категорію до бази даних. Потрібно вказати назву та опис.", tags=["Категорія"])
async def insert_category(category: CategoryCreate,
                          session: AsyncSession = Depends(get_prod_session)
                          ):
        try:
            new_category = await CategoryService.insert_category(
            session=session,
            name=category.name,
            description=category.description
        )
            return new_category
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@category_router.get("/category", 
                    summary="Отримати всі категорії",
                    description="Повертає список усіх наявних категорій у базі.",
                    response_model=List[CategoryResponse], tags=["Категорія"])
async def get_categories(session: AsyncSession = Depends(get_prod_session)):
        try:
            result = await CategoryService.get_all_category(session=session)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
        

@category_router.delete("/category/{category_id}",
                        summary="Видалити категорію",
                        description="Видаляє категорію за ID. Якщо категорію не знайдено — повертає помилку.",
                        tags=["Категорія"])
async def delete_category_by_id(category_id: int, session: AsyncSession = Depends(get_prod_session)):
        try:
            success = await CategoryService.delete_category_by_id(category_id, session=session)
            return {"message": f"Category was deleted, {success}"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
        
@category_router.put("/category/{category_id}", 
                    summary="Оновити категорію",
                    description="Оновлює назву та опис категорії за її ID.",
                    tags=["Категорія"])
async def update_product(category_id: int, category_data: CategoryUpdate, session: AsyncSession = Depends(get_prod_session)):
        updated = await CategoryService.update_category_by_id(
            session=session,
            category_id=category_id,
            name=category_data.name,
            description=category_data.description,
    
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Categiry not found")
        return updated

@category_router.get("/category-products/", 
                    summary="Категорії з товарами",
                    description="Повертає всі категорії разом з пов’язаними товарами.",
                    tags=["Категорія"])
async def get_all_products(session: AsyncSession = Depends(get_prod_session)) -> List[dict]:
    try:
        return await CategoryService.get_products_with_category(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    

@category_router.get("/category/{category_id}", 
                summary="Одна категорія з товарами",
                description="Повертає конкретну категорію з усіма її товарами за ID.", 
                tags=["Категорія"])
async def get_all_products(category_id, session: AsyncSession = Depends(get_prod_session)) -> List[dict]:
    try:
        return await CategoryService.get_category_with_products(session, category_id=category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
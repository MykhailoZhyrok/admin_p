from typing import Dict, List, Optional
from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from app.db.session import async_session_factory
from app.models.product import ProductsOrm
from app.models.category import CategoriesOrm
from app.schemas.category import CategoryResponse
from sqlalchemy.ext.asyncio import AsyncSession

class CategoryService:

    @staticmethod
    async def insert_category(session: AsyncSession, name: str, description: str | None) -> CategoryResponse:
        new_category = CategoriesOrm(name=name, description=description)
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        return CategoryResponse.model_validate(new_category)
    

    @staticmethod
    async def get_all_category(session: AsyncSession) -> CategoryResponse:
        result = await session.execute(select(CategoriesOrm))
        products = result.scalars().all()
        return [CategoryResponse.from_orm(cat) for cat in products]

    @staticmethod
    async def delete_category_by_id(category_id: int, session: AsyncSession):
        category = await session.get(CategoriesOrm, category_id)
        if not category:
            return False
        await session.delete(category)
        await session.commit()
        return True
    
    
    @staticmethod
    async def update_category_by_id(
        session: AsyncSession,
        category_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None, 
       
    ):
        category  = await session.get(CategoriesOrm, category_id)
        if not category:
            return None
        if name is not None:
            category.name = name
        if description is not None:
            category.description = description
        
        await session.flush()
        await session.commit()
        await session.refresh(category)

        return CategoryResponse.model_validate(category)
            

    @staticmethod     
    async def get_category_with_products(session: AsyncSession, category_id) -> List[dict]:
            result = await session.execute(
                select(ProductsOrm)
                .where(ProductsOrm.category_id == category_id)
                .options(selectinload(ProductsOrm.category))
           
            )
            products = result.scalars().all()
            return [
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "category": {
                        "id": product.category.id,
                        "name": product.category.name,
                        "description": product.category.description
                    }
                }
                
                for product in products
            ]
    
  

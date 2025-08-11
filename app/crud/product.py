from typing import Dict, List, Optional
from app.models.category import CategoriesOrm
from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from app.db.session import async_session_factory
from app.models.product import ProductsOrm
from app.schemas.product import ProductResponse
from sqlalchemy.ext.asyncio import AsyncSession

class ProductsService:

    @staticmethod
    async def get_all_products(session: AsyncSession)->ProductResponse:
            result = await session.execute(select(ProductsOrm).options(joinedload(ProductsOrm.category)))
            products = result.scalars().all()
            return [ProductResponse.model_validate(p, from_attributes=True) for p in products]  

        

    @staticmethod
    async def insert_product(session: AsyncSession, name: str, category_id: int, description: Optional[str] = None) -> ProductResponse:
        product = ProductsOrm(name=name, description=description, category_id=category_id)
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return ProductResponse.model_validate(product, from_attributes=True)

    @staticmethod
    async def delete_product_by_id(product_id: int, session: AsyncSession):
        product = await session.get(ProductsOrm, product_id)
        if not product:
            return False
        await session.delete(product)
        await session.commit()
        return True
    
    
    @staticmethod
    async def update_product_by_id(
        session: AsyncSession,
        product_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        category_id: Optional[int] = None,
    ):
                product = await session.get(ProductsOrm, product_id)
                if not product:
                    return None
                if name is not None:
                    product.name = name
                if description is not None:
                    product.description = description
                if category_id is not None:
                        category = await session.get(CategoriesOrm, category_id)
                        if not category:
                            raise ValueError(f"Категорія з ID {category_id} не існує")
                        product.category_id = category_id
                await session.flush()
                await session.commit()
                await session.refresh(product) 
                return ProductResponse.model_validate(product, from_attributes=True)
            
         
    @staticmethod
    async def get_product_by_id(product_id: int, session: AsyncSession,) -> Optional[Dict]:
            result = await session.execute(
                select(ProductsOrm)
                .filter_by(id=product_id)
                .options(selectinload(ProductsOrm.category))
            )
            product = result.scalars().first()
            if not product:
                return None

            return ProductResponse.model_validate(product, from_attributes=True)
    
            
    @staticmethod
    async def get_product_by_id(product_id: int, session: AsyncSession,) -> Optional[Dict]:
            result = await session.execute(
                select(ProductsOrm)
                .filter_by(id=product_id)
                .options(selectinload(ProductsOrm.category))
            )
            product = result.scalars().first()
            if not product:
                return None

            return ProductResponse.model_validate(product, from_attributes=True)
    
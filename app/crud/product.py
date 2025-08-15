from typing import Dict, Optional

from pathlib import Path 
from app.models.category import CategoriesOrm
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from app.models.product import ProductsOrm
from app.schemas.product import ProductData, ProductResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class ProductsService:

    @staticmethod
    async def get_all_products(session: AsyncSession)->ProductResponse:
            result = await session.execute(select(ProductsOrm).options(joinedload(ProductsOrm.category)))
            products = result.scalars().all()
            return [ProductResponse.model_validate(p, from_attributes=True) for p in products]  
    
    @staticmethod
    async def insert_product(
            session: AsyncSession,
            data: ProductData,
        ) -> ProductResponse:
        product = ProductsOrm(**data.model_dump())
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return ProductResponse.model_validate(product, from_attributes=True)

    @staticmethod
    async def delete_product_by_id(product_id: int, session: AsyncSession):
        product = await session.get(ProductsOrm, product_id)
        if not product:
            return False
        if product.image_path:
            file_path = Path("." + product.image_path)  
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                print(f"Не вдалося видалити файл {file_path}: {e}")
        await session.delete(product)
        await session.commit()
        return True

    @staticmethod
    async def update_product_by_id(
        session: AsyncSession,
        product_id: int,
        data: ProductData,
    ):
                product = await session.get(ProductsOrm, product_id)

                update_data = data.model_dump()

                if not product:
                    return None
                
                for field, value in update_data.items():
                    if value is not None:
                        if field == "category_id":
                            category = await session.get(CategoriesOrm, data.category_id)
                            if not category:
                                raise ValueError(f"Категорія з ID {data.category_id} не існує")
                        elif field == "image_path":
                            if product.image_path:
                                file_path = Path("." + product.image_path)  
                                if file_path.exists():
                                    try:
                                        file_path.unlink()
                                    except Exception as e:
                                        print(f"Не вдалося видалити файл {file_path}: {e}")
                        setattr(product, field, value)
                        
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
    
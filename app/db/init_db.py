from app.models.product import ProductsOrm
from app.models.user import UsersOrm
from app.db.session import async_engine_prod, async_engine_user

async def create_tables_prod():
    async with async_engine_prod.begin() as conn:
        await conn.run_sync(ProductsOrm.metadata.drop_all)
        await conn.run_sync(ProductsOrm.metadata.create_all)

async def create_tables_user():
    async with async_engine_user.begin() as conn:
        await conn.run_sync(UsersOrm.metadata.drop_all)
        await conn.run_sync(UsersOrm.metadata.create_all)

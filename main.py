import sys
import asyncio
import uvicorn
from fastapi import FastAPI
# from app.main import create_fastapi_app
from app.db.init_db import create_tables_prod, create_tables_user
from app.api.category import category_router
from app.api.product import product_router
from app.api.user import user_router

app = FastAPI(title="My API")
# app = create_fastapi_app()

app.include_router(user_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1")

async def main():
    await create_tables_prod()
    await create_tables_user()

if __name__ == "__main__":
    asyncio.run(main())


import sys
import asyncio
import uvicorn
from fastapi import Depends, FastAPI
# from app.main import create_fastapi_app
from app.db.init_db import create_tables_prod, create_tables_user
from app.api.category import category_router
from app.api.product import product_router
from app.api.user import user_router
from app.api.cart import cart_router
from app.for_test.test import*
from app.api.order import order_router
from app.utils.dependency import verify_api_key

app = FastAPI(title="My API")
# app = create_fastapi_app()


app.include_router(user_router, prefix="/api/v1", dependencies=[Depends(verify_api_key)])
app.include_router(category_router, prefix="/api/v1", dependencies=[Depends(verify_api_key)])
app.include_router(product_router, prefix="/api/v1", dependencies=[Depends(verify_api_key)])
app.include_router(cart_router, prefix="/api/v1", dependencies=[Depends(verify_api_key)])
app.include_router(order_router, prefix="/api/v1", dependencies=[Depends(verify_api_key)])


async def main():
    await create_tables_prod()
    await create_tables_user()

if __name__ == "__main__":
    asyncio.run(main())


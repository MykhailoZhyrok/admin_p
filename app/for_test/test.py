from sqlalchemy import event
from sqlalchemy.orm import Session
from app.models.category import CategoriesOrm
from app.models.product import ProductsOrm
from app.models.user import UsersOrm
from app.crud.user import bcrypt_context

initial_products = [
    {"name": "Product 1", "description": "Description 1", "category_id": 1, "price": 10.50, "stock_quantity": 100},
    {"name": "Product 2", "description": "Description 2", "category_id": 1, "price": 25.00, "stock_quantity": 50},
]

def insert_initial_products(target, connection, **kw):
    with Session(bind=connection) as session:
        for prod in initial_products:
            session.add(ProductsOrm(**prod))
        session.commit()
        print("start_creating products>>>")


def insert_category(target, connection, **kw):
    with Session(bind=connection) as session:
        new_category = CategoriesOrm(name="owocie", description="owocie_description")
        session.add(new_category)
        session.commit()
        print("start_creating categories>>>")


def create_user(target, connection, **kw):
    with Session(bind=connection) as session:
        new_user = UsersOrm(
        username = "admin",
        hashed_password = bcrypt_context.hash("admin"),

        )
        session.add(new_user)
        session.commit()


print("start_creating>>>")




event.listen(CategoriesOrm.__table__, 'after_create', insert_category)
event.listen(ProductsOrm.__table__, 'after_create', insert_initial_products)
event.listen(UsersOrm.__table__, 'after_create', create_user)


# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from app.models.order import OrderOrm, OrderItemOrm
# from app.models.product import ProductsOrm
# import asyncio

# # SQLite (источник)
# SQLITE_URL = "sqlite+aiosqlite:///products.db"
# sqlite_engine = create_async_engine(SQLITE_URL, echo=False)
# SQLiteSession = sessionmaker(sqlite_engine, expire_on_commit=False, class_=AsyncSession)

# # PostgreSQL (приёмник)
# POSTGRES_URL = "postgresql+asyncpg://postgres:password@localhost:5432/products_db"
# postgres_engine = create_async_engine(POSTGRES_URL, echo=False)
# PostgresSession = sessionmaker(postgres_engine, expire_on_commit=False, class_=AsyncSession)
# async def migrate_orders():
#     async with SQLiteSession() as sqlite_session, PostgresSession() as pg_session:
#         # 1. Продукты
#         products = await sqlite_session.execute(select(ProductsOrm))
#         products_list = products.scalars().all()
#         for p in products_list:
#             pg_session.add(
#                 ProductsOrm(
#                     id=p.id,
#                     name=p.name,
#                     description=p.description,
#                     category_id=p.category_id,
#                     price=p.price,
#                     is_active=p.is_active,
#                     stock_quantity=p.stock_quantity,
#                     image_path=p.image_path,
#                     created_at=p.created_at,
#                     updated_at=p.updated_at
#                 )
#             )
#         await pg_session.commit()

#         # 2. Заказы
#         orders = await sqlite_session.execute(select(OrderOrm))
#         orders_list = orders.scalars().all()
#         for o in orders_list:
#             pg_session.add(
#                 OrderOrm(
#                     id=o.id,
#                     public_id=o.public_id,
#                     user_id=o.user_id,
#                     session_token=o.session_token,
#                     status=o.status,
#                     subtotal=o.subtotal,
#                     currency=o.currency,
#                     created_at=o.created_at,
#                     updated_at=o.updated_at
#                 )
#             )
#         await pg_session.commit()

#         # 3. Элементы заказов
#         order_items = await sqlite_session.execute(select(OrderItemOrm))
#         items_list = order_items.scalars().all()
#         for item in items_list:
#             pg_session.add(
#                 OrderItemOrm(
#                     id=item.id,
#                     order_id=item.order_id,
#                     product_id=item.product_id,
#                     quantity=item.quantity,
#                     unit_price=item.unit_price
#                 )
#             )
#         await pg_session.commit()

# async def main():

#     await migrate_orders()
#     print("Migration finished!")

# main()
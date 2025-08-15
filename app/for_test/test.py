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

def insert_category(target, connection, **kw):
    with Session(bind=connection) as session:
        new_category = CategoriesOrm(name="owocie", description="owocie_description")
        session.add(new_category)
        session.commit()

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



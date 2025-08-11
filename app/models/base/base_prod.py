from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

class BaseProd(DeclarativeBase):
    pass


metadata_obj = MetaData()
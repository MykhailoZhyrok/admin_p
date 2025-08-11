from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import DeclarativeBase

class BaseUser(DeclarativeBase): pass


metadata_obj = MetaData()
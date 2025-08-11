from pydantic import BaseModel
from typing import Optional

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None 



class CategoryResponse(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    class Config:
        from_attributes = True
        
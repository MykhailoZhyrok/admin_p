from pydantic import BaseModel
from typing import Optional

class CurrentUser(BaseModel):
    username: str
    id: int

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    username: str
    hashed_password: str
    id: int



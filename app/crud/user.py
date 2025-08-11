from datetime import timedelta, datetime 
from typing import Annotated, List
from app.models.user import  UsersOrm
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from app.schemas.user import CreateUserRequest, CurrentUser

SECRET_KEY = "SECRET_KEY"
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2bearer = OAuth2PasswordBearer(tokenUrl='/api/v1/user/token')

class UserService:
    @staticmethod
    async def authenticate_user(session: AsyncSession, username: str, password: str):
        try:
            result = await session.execute(
                select(UsersOrm).filter_by(username=username)
            )
            user = result.scalar_one_or_none()
            if not user or not bcrypt_context.verify(password, user.hashed_password):
                return None
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail="Database error occurred")
    
    @staticmethod
    def create_access_token(username: str, user_id: int, expires_delta: timedelta):
        encode = {'sub': username, 'id':user_id}
        expires = datetime.utcnow()+expires_delta
        encode.update({'exp': expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2bearer)]) -> CurrentUser:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get('sub')
            user_id: int = payload.get('id')
            if username is None or user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token payload")
            return CurrentUser(username=username, id=user_id)
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    @staticmethod
    async def create_user(session: AsyncSession, create_user_request:CreateUserRequest):
        new_user = UsersOrm(
        username = create_user_request.username,
        hashed_password = bcrypt_context.hash(create_user_request.password),

        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return create_user_request

    @staticmethod
    async def get_all_users(session: AsyncSession)->List[CreateUserRequest]:
            result = await session.execute(select(UsersOrm))
            users = result.scalars().all()
            return users




from datetime import timedelta
from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import UserService
from app.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.crud.product import ProductsService  
from app.db.session import get_prod_session, get_user_session 
from app.schemas.product import ProductResponse, ProductCreate
from app.schemas.user import CreateUserRequest, CurrentUser, Token, UserResponse


user_router = APIRouter()


# @user_router.get("/login", tags=["User"])
# async def user(user: CreateUserRequest, session: AsyncSession = Depends(get_prod_session)):
#     if user is None: 
#         raise HTTPException(status_code=401, detail="Authentication Failed")
#     return {"User": user}


@user_router.post("/user/token", response_model=Token, tags=["User"], summary="Login to obtain an access token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_user_session)):
    user = await UserService.authenticate_user(session, form_data.username, form_data.password)
    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    
    token = UserService.create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}
    

@user_router.get("/user/get", tags=["User"], response_model=List[UserResponse])
async def get_all_users( session: AsyncSession = Depends(get_user_session)):
    users = await UserService.get_all_users(session)
    if not users:
        raise HTTPException(status_code=400, detail="Users not found")
    return users



@user_router.post("/user/sign-up", tags=["User"], response_model=CreateUserRequest)
async def create_user(
    create_user_request: CreateUserRequest,
    session: AsyncSession = Depends(get_user_session)):
    user = await UserService.create_user(
        session,
        create_user_request
    )

    if not user:
        raise HTTPException(status_code=400, detail="User not created")
    return user





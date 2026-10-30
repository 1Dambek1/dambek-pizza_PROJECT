
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy import select
from src.db import get_session
from src.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import CreateUser
from .utils import create_acces_token, hash_password, check_password
from .get_user import get_current_user
app = APIRouter(prefix="/users",tags=["users"])


@app.post("/register")
async def register(user_data:CreateUser,
                   session:AsyncSession = Depends(get_session)):
 user = User(**user_data.model_dump())
 user.password = await hash_password(user.password)
 session.add(user)
 await session.flush()
 jwt = await create_acces_token(user.id)
 await session.commit()
 return jwt


@app.get("/get")
async def get_user(user:User = Depends(get_current_user),session:AsyncSession = Depends(get_session)):
 return user

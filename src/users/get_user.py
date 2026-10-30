from fastapi import Depends, HTTPException
from sqlalchemy import select
from src.db import get_session
from src.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import  decode_acces_token

async def get_current_user(token:str,session:AsyncSession = Depends(get_session)):
  key = await decode_acces_token(token)
  if not key:
   raise HTTPException(status_code=403)
  user = await session.scalar(select(User).where(User.id == key))
  return user

async def get_admin(user = Depends(get_current_user)):
 if user.status == "admin":
  return user
 raise HTTPException(status_code=403)


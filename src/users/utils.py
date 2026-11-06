import datetime
import uuid
from fastapi import Depends
import jwt
from pwdlib import PasswordHash
from sqlalchemy import select
from src.config import config
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_session
from src.models.session import Sessions

password_hash = PasswordHash.recommended()


async def hash_password(password) -> str:
 return password_hash.hash(password)


async def check_password(password:str, hashed_password:str) -> bool:
 return password_hash.verify(password,hashed_password) # True\False



async def create_acces_token(user_id:int,session:AsyncSession) -> str:
 key = uuid.uuid4()
 session_db = Sessions(user_id = user_id,id = key , exp = datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=30))
 session.add(session_db)

 return key


async def decode_acces_token(token:uuid.UUID,session:AsyncSession) -> int| None:
 now = datetime.datetime.now(datetime.timezone.utc)
 ses = await session.scalar(select(Sessions).where(Sessions.id == token))
 if not ses:
  return None
 exp = ses.exp.replace(tzinfo=datetime.timezone.utc)
 if exp <= now:
  return None
 return int(ses.user_id)

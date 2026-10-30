import datetime
import jwt
from pwdlib import PasswordHash
from src.config import config

password_hash = PasswordHash.recommended()


async def hash_password(password) -> str:
 return password_hash.hash(password)


async def check_password(password:str, hashed_password:str) -> bool:
 return password_hash.verify(password,hashed_password) # True\False



async def create_acces_token(user_id:int) -> str:
 now = datetime.datetime.now(datetime.timezone.utc)

 payload = {
  "user_id": user_id,
  "iat":now,
  'exp': now + datetime.timedelta(minutes=30)
 }
 return jwt.encode(payload,config.auth_config.SECRET_KEY,config.auth_config.ALGORITHM)


async def decode_acces_token(token:str) -> int| None:
 try:
  payload = jwt.decode(
   token,config.auth_config.SECRET_KEY,[config.auth_config.ALGORITHM]
  )
  return int(payload["user_id"])
 except:
  return None

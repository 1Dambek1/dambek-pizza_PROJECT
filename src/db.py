from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.config import config

engine = create_async_engine(config.db_config.DATABASE_URL, echo=True)

Session = sessionmaker(engine, class_=AsyncSession)


class Base(DeclarativeBase):
 ...


async def get_session():
 async with Session() as s:
  yield s

async def create_db():
 async with engine.begin() as conn:
  await conn.run_sync(Base.metadata.drop_all)
  await conn.run_sync(Base.metadata.create_all)



import json
import random

import fastapi
from pydantic import BaseModel
from sqlalchemy import insert, select
from src.db import create_db
from src.users.router import app as user_app
from .utils import r

from fastapi import Depends
from src.db import get_session
from src.models.pizza import Pizza
from sqlalchemy.ext.asyncio import AsyncSession
import time

app = fastapi.FastAPI(title="WinPizza")
app.include_router(user_app)
# /action/what

@app.get("/echo")
async def echo():
 return True

@app.get("/create/db")
async def create_db_action():
 await create_db()
 return True


@app.get("/redis")
async def redis_check():
 await r.set("name","Jhon")
 return await r.get("name")

@app.post("/generate")
async def generate_pizzas(
    session: AsyncSession = Depends(get_session)
):
    names = [
        "Маргарита", "Пепперони", "Четыре сыра",
        "Гавайская", "Мясная", "Барбекю",
        "Карбонара", "Охотничья"
    ]

    pizzas = [
        {
            "name": f"{random.choice(names)} #{i}",
            "price": round(random.uniform(300, 1500), 2),
            "description": f"Вкусная пицца номер {i}"
        }
        for i in range(10_000)
    ]

    await session.execute(insert(Pizza), pizzas)
    await session.commit()

    return {"created": len(pizzas)}



@app.get("/pizzas")
async def get_pizzas(session: AsyncSession = Depends(get_session)):
 times = time.time()
 data = await r.get("pizzas_cache")
 if not data:
  data = (await session.scalars(select(Pizza))).all()
  data = [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "description": p.description
            }
            for p in data
        ]

  await r.set("pizzas_cache", json.dumps(data),ex = 60)
 else:
  data = json.loads(data)

 return time.time() - times


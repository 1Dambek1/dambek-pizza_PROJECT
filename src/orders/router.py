import json
import time

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import selectinload
from src.db import get_session
import random
from sqlalchemy import delete, insert, select
from src.models.pizza import Pizza
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.basket import Size, Basket
from src.models.users import User
from src.users.get_user import get_current_user
from fastapi import HTTPException
from src.models.orders import Items, Order
app = APIRouter(prefix="/pizza", tags=["pizza"])


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



@app.get("/get/pizzas")
async def get_pizzas(limit:int, offset:int,session: AsyncSession = Depends(get_session)):
 data = (await session.scalars(select(Pizza).limit(limit).offset(offset)) ).all()
 return data



@app.post("/add/basket")
async def add_basket(pizza_id:int,size:Size,user:User = Depends(get_current_user),session: AsyncSession = Depends(get_session)):
   pizza = await session.scalar(select(Pizza).where(Pizza.id == pizza_id))
   if not pizza:
      raise HTTPException()
   basket = await session.scalar(select(Basket).where(Basket.user_id == user.id, Basket.pizza_id == pizza_id))
   if basket:
      basket.count +=1
      await session.commit()
      return True
   basket = Basket(pizza_id = pizza_id, user_id = user.id, size = size)
   session.add(basket)
   await session.commit()
   return True


@app.get("/get/backet")
async def geg_backet(user:User = Depends(get_current_user),session: AsyncSession = Depends(get_session)):
   user_data = await session.scalars(select(Basket).where(Basket.user_id == user.id).options(selectinload(Basket.pizza)))
   return user_data.all()

@app.get("/get/price/backet")
async def geg_backet(user:User = Depends(get_current_user),session: AsyncSession = Depends(get_session)):
   user_data = await session.scalars(select(Basket).where(Basket.user_id == user.id).options(selectinload(Basket.pizza)))
   a = [basket.pizza.price*basket.count for basket in user_data]
   sums = sum(a)
   counts= sum(basket.count for basket in user_data)
   return {"items":counts, "total_sum":sums}

@app.post("/create/order")
async def create_order(adress:str,user:User = Depends(get_current_user),session: AsyncSession = Depends(get_session)):
   baskets = await session.scalars(select(Basket).where(Basket.user_id == user.id))
   if not baskets:
      raise HTTPException()

   order = Order(adress= adress,user_id = user.id)
   session.add(order)
   await session.flush()
   for basket in baskets:
     item = Items(pizza_id = basket.pizza_id,
                  size = basket.size,
                  count = basket.count,
                  order_id = order.id)
     session.add(item)
   await session.execute(delete(Basket).where(Basket.user_id == user.id))
   await session.commit()
   return True


@app.get("/get/orders")
async def get_orders(user:User = Depends(get_current_user),session: AsyncSession = Depends(get_session)):
 orders = await session.scalars(select(Order)
                                .where(Order.user_id == user.id)
                                .options(selectinload(Order.items).selectinload(Items.pizza)))
 return orders.all()


@app.get("/get/orders/{id}")
async def get_order(idx:int,user:User = Depends(get_current_user),session: AsyncSession = Depends(get_session)):
 orders = await session.scalar(select(Order)
                                .where(Order.user_id == user.id, Order.id == idx)
                                .options(selectinload(Order.items).selectinload(Items.pizza)))
 return orders

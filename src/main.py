import fastapi
from src.db import create_db
from src.users.router import app as user_app

from src.orders.router import app as pizza_app
app = fastapi.FastAPI(title="WinPizza")
app.include_router(user_app)

app.include_router(pizza_app)


# /action/what

@app.get("/echo")
async def echo():
 return True

@app.get("/create/db")
async def create_db_action():
 await create_db()
 return True


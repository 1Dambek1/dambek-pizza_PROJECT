import uuid

from fastapi import APIRouter, WebSocket

from sqlalchemy import select
from src.db import Session
from src.models.messages import Message
app = APIRouter(tags=["chats"] ,prefix="/chats")

chats = {}
# ws - webscoket
@app.websocket("/ws/chat/{idx}")
async def chat(idx:uuid.UUID,webcoscket:WebSocket):
 await webcoscket.accept()
 chats[idx] = chats.get(idx, [])
 chats[idx].append(webcoscket)
 async with Session() as s:
  messges = await s.scalars(select(Message).where(Message.chat_id == idx).limit(50))
  await webcoscket.send_json({
   "type":"history",
   "messages":[m.message for m in messges]
  })
 try:
  while True:

   data = await webcoscket.receive_text()
   async with Session() as s:
    message = Message(chat_id = idx, message = data)
    s.add(message)
    await s.commit()
   for i in chats[idx]:
    if i != webcoscket:
     await i.send_json({"type":"new", "message":f"{data} good"})
 except:
  await webcoscket.close()

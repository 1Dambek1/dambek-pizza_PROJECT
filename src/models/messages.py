import uuid

from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

import enum
from sqlalchemy import Enum
from src.models.pizza import Pizza

class Message(Base):
 __tablename__ = 'messages'
 id:Mapped[int] = mapped_column(primary_key= True)
 chat_id:Mapped[uuid.UUID]
 message:Mapped[str]


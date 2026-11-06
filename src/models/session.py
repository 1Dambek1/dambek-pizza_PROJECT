
import datetime
import uuid
from sqlalchemy import ForeignKey
from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column
class Sessions(Base):
 __tablename__ = "sessions"

 id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
 user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

 exp:Mapped[datetime.datetime]

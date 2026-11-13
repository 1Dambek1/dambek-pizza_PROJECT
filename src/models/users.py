from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .pizza import Pizza
class User(Base):
 __tablename__ = 'user'
 id:Mapped[int] = mapped_column(primary_key= True)

 username:Mapped[str]

 name:Mapped[str]
 surname:Mapped[str]
 address:Mapped[str]

 password:Mapped[str]

 basket:Mapped[list["Pizza"]] = relationship(uselist=True,secondary="basket")

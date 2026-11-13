from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

import enum
from sqlalchemy import Enum
from src.models.pizza import Pizza

class Size(str,enum.Enum):
 small = "sm"
 medium ="md"
 large = "l"
 super_large = "xl"

class Items(Base):
 __tablename__ = 'items'
 id:Mapped[int] = mapped_column(primary_key= True)


 pizza_id:Mapped[int] = mapped_column(ForeignKey("pizza.id"))
 pizza:Mapped["Pizza"] = relationship(uselist=False)

 size:Mapped[Size] = mapped_column(
  Enum(Size),
  default=Size.medium
 )
 count:Mapped[int] = mapped_column(default=1)

 order_id:Mapped[int] = mapped_column(ForeignKey("order.id"))

class Order(Base):
 __tablename__ = 'order'
 id:Mapped[int] = mapped_column(primary_key= True)
 items:Mapped[list["Items"]] = relationship(uselist=True)
 user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
 adress:Mapped[str]



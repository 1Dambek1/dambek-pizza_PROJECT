from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

# import enum
# from sqlalchemy import Enum
# class Size(str,enum.Enum):
#  small = "sm"
#  medium ="md"
#  large = "l"
#  super_large = "xl"


class Category(Base):
 __tablename__ = "category"
 id:Mapped[int] = mapped_column(primary_key=True)
 name:Mapped[str]
 products:Mapped[list["Pizza"]] = relationship(uselist=True)

class Pizza(Base):
 __tablename__ = 'pizza'
 id:Mapped[int] = mapped_column(primary_key= True)

 name:Mapped[str]
 price:Mapped[float]
 description:Mapped[str]

 cat_id:Mapped[int] = mapped_column(ForeignKey("category.id"))



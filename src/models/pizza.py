from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column

# import enum
# from sqlalchemy import Enum
# class Size(str,enum.Enum):
#  small = "sm"
#  medium ="md"
#  large = "l"
#  super_large = "xl"



class Pizza(Base):
 __tablename__ = 'pizza'
 id:Mapped[int] = mapped_column(primary_key= True)

 name:Mapped[str]
 price:Mapped[float]
 description:Mapped[str]
 # sizes:Mapped[Size] = mapped_column(
 #  Enum(Size),
 #  default=Size.medium
 # )


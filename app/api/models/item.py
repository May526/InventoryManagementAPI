from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from api.db import Base


class item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255),unique=True,index=True)
    amount = Column(Integer)
    price = Column(Float)

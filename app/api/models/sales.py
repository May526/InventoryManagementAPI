from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship

from api.db import Base

class sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    sales = Column(Float, index=True)
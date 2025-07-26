from sqlalchemy import Column, Integer, String
from app.database import Base

class FlowerTable(Base):
    __tablename__ = "flowers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    species = Column(String(255))
    color = Column(String(255))

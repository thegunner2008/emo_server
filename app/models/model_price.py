from app.models import Base
from sqlalchemy import Column, Integer


class Price(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

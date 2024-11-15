from app.models import Base
from sqlalchemy import Column, Integer


class Price(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models import model_transaction
from app.models.model_base import BareBaseModel


class Job(BareBaseModel):
    key_word = Column(String, nullable=False)
    image = Column(String, nullable=False)
    total = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    reset_day = Column(Integer, nullable=False)
    factor = Column(Float, nullable=False)
    base_url = Column(String, nullable=False)
    url = Column(String, nullable=False)
    key_page = Column(String, nullable=False)
    value_page = Column(String, nullable=False)
    time = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)
    finish_at = Column(DateTime, nullable=True, default=None)
    current = relationship("Current", back_populates='job', uselist=False)

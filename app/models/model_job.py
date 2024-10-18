from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class Job(BareBaseModel):
    key_word = Column(String(150), nullable=False)
    image = Column(String(255), nullable=False)
    total = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    max_day = Column(Integer, nullable=False)
    reset_day = Column(Integer, nullable=False)
    factor = Column(Float, nullable=False)
    base_url = Column(String(50), nullable=False)
    url = Column(String(100), nullable=False)
    key_page = Column(String(150), nullable=False)
    value_page = Column(String(150), nullable=False)
    time = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)
    finish_at = Column(DateTime, nullable=True, default=None)
    current = relationship("Current", back_populates='job', uselist=False)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    user = relationship("User")

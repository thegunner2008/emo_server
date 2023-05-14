from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models import user_job
from app.models.model_base import BareBaseModel


class Job(BareBaseModel):
    key_word = Column(String, nullable=False)
    image = Column(String, nullable=False)
    total = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    base_url = Column(String, nullable=False)
    url = Column(String, nullable=False)
    key_page = Column(String, nullable=False)
    value_page = Column(String, nullable=False)
    time = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)
    finish_at = Column(DateTime, nullable=True, default=None)
    users = relationship("UserJob", back_populates='job')
    current = relationship("Current", back_populates='job', uselist=False)

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey

from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class Total(BareBaseModel):
    user_id = Column(ForeignKey('user.id'), primary_key=True)
    user = relationship('User')
    total = Column(Integer)
    count_transaction = Column(Integer)
    count_job = Column(Integer)
    withdraw_total = Column(Integer)
    withdraw_count = Column(Integer)

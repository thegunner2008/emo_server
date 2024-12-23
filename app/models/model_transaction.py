from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class Transaction(BareBaseModel):
    user_id = Column(ForeignKey('user.id'), primary_key=True)
    job_id = Column(ForeignKey('job.id'), primary_key=True)
    user = relationship("User")
    job = relationship("Job")
    money = Column(Integer)
    ip = Column(String(20))
    device_id = Column(String(50))
    time_int = Column(Integer)
    description = Column(String(255))

    Index('idx_transaction_device_time', device_id, time_int)

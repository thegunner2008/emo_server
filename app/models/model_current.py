from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey

from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class Current(BareBaseModel):
    user_id = Column(ForeignKey('user.id'), primary_key=True)
    user = relationship('User', back_populates='current')
    job_id = Column(ForeignKey('job.id'))
    job = relationship('Job', back_populates='current')

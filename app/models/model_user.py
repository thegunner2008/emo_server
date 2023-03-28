from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey

from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class User(BareBaseModel):
    user_name = Column(String, nullable=False)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String, default='guest')
    last_login = Column(DateTime)
    jobs = relationship('UserJob', back_populates='user')
    current = relationship('Current', back_populates='user', uselist=False)
    withdraws = relationship('Withdraw', back_populates='user')

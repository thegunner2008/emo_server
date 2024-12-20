from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey

from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class User(BareBaseModel):
    user_name = Column(String(150), nullable=False)
    full_name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default='guest')
    last_login = Column(DateTime)
    current = relationship('Current', back_populates='user', uselist=False)

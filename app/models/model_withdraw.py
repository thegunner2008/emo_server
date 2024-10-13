from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.enum.enum_withdraw import StatusWithdraw
from app.models.model_base import BareBaseModel


class Withdraw(BareBaseModel):
    description = Column(String(255))
    reply = Column(String(255))
    url_clue = Column(String(255))
    image_clue = Column(String(255))
    money = Column(Integer, nullable=False)
    withdraw_method = Column(String(150), nullable=False)
    bank_key = Column(Integer, nullable=False)
    number_account = Column(String(150), nullable=False)
    account_name = Column(String(150), nullable=False)
    status = Column(Enum(StatusWithdraw))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")


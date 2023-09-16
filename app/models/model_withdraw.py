from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.enum.enum_withdraw import StatusWithdraw
from app.models.model_base import BareBaseModel


class Withdraw(BareBaseModel):
    description = Column(String)
    reply = Column(String)
    url_clue = Column(String)
    image_clue = Column(String)
    money = Column(Integer, nullable=False)
    withdraw_method = Column(String, nullable=False)
    bank_key = Column(Integer, nullable=False)
    number_account = Column(String, nullable=False)
    account_name = Column(String, nullable=False)
    status = Column(Enum(StatusWithdraw))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")


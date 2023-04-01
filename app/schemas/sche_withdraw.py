from pydantic import BaseModel

from app.enum.enum_withdraw import StatusWithdraw


class WithdrawCreate(BaseModel):
    description: str
    money: int
    withdraw_method = str
    bank_name = str
    number_account: str
    account_name: str
    status: str = StatusWithdraw.requested
    pass


class WithdrawReply(BaseModel):
    id: str
    reply: str
    url_clue: str
    image_clue: str
    status: str = StatusWithdraw.transferred
    user_id: int

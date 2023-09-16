from pydantic import BaseModel

from app.enum.enum_withdraw import StatusWithdraw


class WithdrawCreate(BaseModel):
    description: str
    money: int
    withdraw_method: str
    bank_key: int
    number_account: str
    account_name: str
    status: str = StatusWithdraw.requested
    pass


class WithdrawPay(BaseModel):
    id: str
    reply: str
    status: str = StatusWithdraw.transferred
    user_id: int

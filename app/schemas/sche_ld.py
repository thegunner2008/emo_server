from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import time

from app.helpers.enums import UserRole
from app.helpers.time_int import now_int, add_time


class RegisterRequest(BaseModel):
    user_name: str
    full_name: str
    password: str
    phone: str
    role: UserRole = UserRole.GUEST


class DeviceLd(BaseModel):
    name: Optional[str] = ''
    start: int = now_int()
    exp: int = add_time(datetime.now(), timedelta(days=1))
    debt_month: int = 0
    is_free: bool = True
    manager_id: str = "0"


class LdRequest(BaseModel):
    manager_id: int = 0
    device_id: str = ''


class LdExtendFree(BaseModel):
    device_id: str = ''


class LdUpdate(BaseModel):
    exp: int = None
    name: str = None
    is_free: bool = True
    manager_id: str = None
    debt_month: int = None


class LdTransfer(BaseModel):
    from_id: int
    to_id: int


class LdPayment(BaseModel):
    device_id: str


class LdPaymentAll(BaseModel):
    device_ids: list

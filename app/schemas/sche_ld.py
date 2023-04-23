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
    exp: int = add_time(datetime.now(), timedelta(days=7))
    paid_time: int = exp
    type: str = 'Free'
    manager_id: str = "1"


class LdRequest(BaseModel):
    manager_id: int = 1
    device_id: str = ''


class LdUpdate(BaseModel):
    exp: int = None
    name: str = None
    type: str = None
    manager_id: str = None


class LdTransfer(BaseModel):
    from_id: int
    to_id: int


class LdPayment(BaseModel):
    device_id: str
    add_time: int

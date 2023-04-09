from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import time

from app.helpers.enums import UserRole


class RegisterRequest(BaseModel):
    user_name: str
    full_name: str
    password: str
    role: UserRole = UserRole.GUEST


class DeviceLd(BaseModel):
    name: Optional[str] = ''
    start: int = int(time.mktime(datetime.now().timetuple()))
    exp: int = int(time.mktime((datetime.now() + timedelta(days=7)).timetuple()))
    type: str = 'Free'
    manager_id: str


class LdRequest(BaseModel):
    manager_id: int = 1
    device_id: str = ''


class LdUpdate(BaseModel):
    exp: int
    name: str
    type: str

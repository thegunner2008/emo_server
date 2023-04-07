from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import time


class DeviceLd(BaseModel):
    name: Optional[str] = ''
    start: int = int(time.mktime(datetime.now().timetuple()))
    exp: int = int(time.mktime((datetime.now() + timedelta(days=7)).timetuple()))
    manager_id: str

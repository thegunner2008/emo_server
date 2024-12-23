from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class JobBase(BaseModel):
    key_word: str
    is_stop: bool
    max_day: int
    total: int
    count: int
    user_id: int
    url: str
    time: int
    money: str
    base_url: str
    reset_day: int
    factor: float


class JobPrepare(BaseModel):
    key_search: str
    url: str


class JobCreate(JobBase):
    key_page: str
    value_page: str
    price: int
    finish_at: Optional[datetime]
    pass


class JobEdit(BaseModel):
    key_word: Optional[str] = None
    is_stop: Optional[bool] = None
    max_day: Optional[int] = None
    total: Optional[int] = None
    count: Optional[int] = None
    user_id: Optional[int] = None
    url: Optional[str] = None
    time: Optional[int] = None
    money: Optional[str] = None
    base_url: Optional[str] = None
    reset_day: Optional[int] = None
    factor: Optional[float] = None
    key_page: Optional[str] = None
    value_page: Optional[str] = None
    price: Optional[int] = None
    finish_at: Optional[datetime] = None
    pass


class JobUpdate(BaseModel):
    max_day: int
    total: int
    time: int
    money: str
    url: str
    price: int
    finish_at: Optional[datetime]


class JobItemResponse(JobBase):
    id: int
    finish_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    key_page: str
    value_page: str

    # users = relationship("User")
    class Config:
        orm_mode = True


class JobStart(JobBase):
    id: int
    user_id: int
    current_id: int


class JobFinish(BaseModel):
    token: str
    value_page: str
    imei: str


class JobTool(BaseModel):
    id: int
    user_id: int
    imei: str
    ip: str
    description: str
    created_at: Optional[datetime]


class JobCancel(BaseModel):
    imei: str

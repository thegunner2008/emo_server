from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class JobBase(BaseModel):
    key_word: str
    image: str
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


class JobCreate(JobBase):
    key_page: str
    value_page: str
    finish_at: Optional[datetime]
    pass


class JobUpdate(BaseModel):
    max_day: int
    total: int
    time: int
    money: str
    url: str
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

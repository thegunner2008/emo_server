from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from app.helpers.exception_handler import CustomException
from app.services.srv_ld import LdService

router = APIRouter()


class LdRequest(BaseModel):
    manager_id: int = 0
    device_id: str = ''


@router.post('')
def get(form_data: LdRequest) -> Any:
    try:
        LdService.create_new_ld(device_id=form_data.device_id, manager_id=form_data.manager_id)
        return True
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))

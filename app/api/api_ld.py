from typing import Any

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel

from app.api.api_login import LoginRequest
from app.core.security import create_access_token
from app.helpers.login_manager import PermissionRequired, login_required, login_required_ld
from app.schemas.sche_base import DataResponse
from app.schemas.sche_ld import LdUpdate, LdRequest, RegisterRequest
from app.services.srv_ld import LdService
from app.schemas.sche_token import Token

router = APIRouter()


@router.post('')
def post(form_data: LdRequest):
    return LdService.create_new_ld(device_id=form_data.device_id, manager_id=form_data.manager_id)


@router.post('/login', response_model=DataResponse[Token])
def login_access_token(form_data: LoginRequest):
    user = LdService.authenticate(email=form_data.userName, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password')

    return DataResponse().success_response({
        'accessToken': create_access_token(user_id=user['id']),
        'user': user,
    })


@router.post('/update', dependencies=[Depends(login_required_ld)])
def update(form_data: LdUpdate,
           device_id: str = Query(..., description="The device to update the LD for")
           ):
    return LdService.update_ld(device_id=device_id, form_data=form_data)


@router.post('/register')
def update_me(form_data: RegisterRequest,
              user_id: str = Query(..., description="The user_id to update the LD for")
              ):
    print(form_data)
    return LdService.update_account(user_id=user_id, form_data=form_data)

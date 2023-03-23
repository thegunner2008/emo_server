from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi_sqlalchemy import db
from pydantic import EmailStr, BaseModel

from app.core.security import create_access_token
from app.helpers.login_manager import PermissionRequired, login_required
from app.models import User
from app.schemas.sche_base import DataResponse
from app.schemas.sche_token import Token
from app.services.srv_user import UserService

router = APIRouter()


@router.post('', dependencies=[Depends(login_required)])
def logout(current_user: User = Depends(UserService.get_current_user)):
    return DataResponse().success_response({})

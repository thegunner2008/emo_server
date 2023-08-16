import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy.orm import joinedload, contains_eager

from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate
from app.models.model_total import Total
from app.models.model_transaction import Transaction
from app.schemas.sche_base import DataResponse
from app.schemas.sche_user import UserItemResponse, UserCreateRequest, UserUpdateMeRequest, UserUpdateRequest
from app.services.srv_user import UserService
from app.models import User, Current

logger = logging.getLogger()
router = APIRouter()


@router.get("")
def get(params: PaginationParams = Depends()) -> Any:
    """
    API Get list User
    """
    try:
        query = db.session.query(User.id, User.email, User.user_name, User.full_name, User.created_at, User.updated_at,
                                 User.last_login, Total.total, Total.count_transaction, Total.count_job,
                                 Total.withdraw_count, Total.withdraw_total).outerjoin(Total, User.id == Total.user_id)
        users = paginate(model=User, query=query, params=params)
        return users
    except Exception as e:
        return CustomException(http_code=400, code='400', message=str(e))


@router.post("", response_model=DataResponse[UserItemResponse])
def create(user_data: UserCreateRequest) -> Any:
    """
    API Create User
    """
    try:
        exist_user = db.session.query(User).filter(User.email == user_data.email).first()
        if exist_user:
            raise Exception('Email already exists')
        new_user = UserService().create_user(user_data)
        return DataResponse().success_response(data=new_user)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.get("/me", dependencies=[Depends(login_required)], response_model=DataResponse[UserItemResponse])
def detail_me(current_user: User = Depends(UserService().get_current_user)) -> Any:
    """
    API get detail current User
    """
    return DataResponse().success_response(data=current_user)


@router.put("/me", dependencies=[Depends(login_required)], response_model=DataResponse[UserItemResponse])
def update_me(user_data: UserUpdateMeRequest,
              current_user: User = Depends(UserService().get_current_user)) -> Any:
    """
    API Update current User
    """
    try:
        if user_data.email is not None:
            exist_user = db.session.query(User).filter(
                User.email == user_data.email, User.id != current_user.id).first()
            if exist_user:
                raise Exception('Email already exists')
        updated_user = UserService().update_me(data=user_data, current_user=current_user)
        return DataResponse().success_response(data=updated_user)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.get("/{user_id}", dependencies=[Depends(login_required)])
def detail(user_id: int) -> Any:
    """
    API get Detail User
    """
    try:
        user = db.session.query(User.id, User.email, User.user_name, User.full_name, User.created_at,
                                User.updated_at,
                                User.last_login, Total.total, Total.count_transaction, Total.count_job,
                                Total.withdraw_count, Total.withdraw_total) \
            .filter(User.id == user_id).outerjoin(Total, Total.user_id == user_id).first()

        if user is None:
            raise Exception('User already exists')

        return DataResponse().success_response(data=user)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.put("/{user_id}", dependencies=[Depends(PermissionRequired('admin'))],
            response_model=DataResponse[UserItemResponse])
def update(user_id: int, user_data: UserUpdateRequest) -> Any:
    """
    API update User
    """
    try:
        exist_user = db.session.query(User).get(user_id)
        if exist_user is None:
            raise Exception('User already exists')
        updated_user = UserService().update(user=exist_user, data=user_data)
        return DataResponse().success_response(data=updated_user)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))

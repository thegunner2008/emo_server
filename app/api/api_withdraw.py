from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate
from app.models import User, Job
from app.models.model_withdraw import Withdraw
from app.models.model_transaction import Transaction
from app.schemas.sche_base import DataResponse

from fastapi_sqlalchemy import db

from app.schemas.sche_withdraw import WithdrawCreate, WithdrawReply
from app.services.srv_user import UserService

router = APIRouter()


@router.get("", dependencies=[Depends(login_required)])
def get(params: PaginationParams = Depends(), current_user: User = Depends(UserService().get_current_user)) -> Any:
    try:
        _query = db.session.query(Withdraw).filter_by(user_id=current_user.id)
        withdraws = paginate(model=Withdraw, query=_query, params=params)
        return withdraws
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.get("/all", dependencies=[Depends(PermissionRequired('admin'))])
def get_all(params: PaginationParams = Depends()) -> Any:
    try:
        _query = db.session.query(Withdraw).options(
            joinedload(Withdraw.user)
        )
        withdraws = paginate(model=Withdraw, query=_query, params=params)
        return withdraws
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.post("", dependencies=[Depends(login_required)])
def post(withdraw: WithdrawCreate, current_user: User = Depends(UserService().get_current_user)):
    current_user_id = current_user.id
    _query_total_money = db.session.query(func.sum(Job.money)).join(Transaction, Job.id == Transaction.job_id).filter(
        Transaction.user_id == current_user_id)
    _total_money = _query_total_money.scalar() or 0

    _query_total_withdraw = db.session.query(func.sum(Withdraw.money)).filter(Withdraw.user_id == current_user_id)
    _total_withdraw = _query_total_withdraw.scalar() or 0
    if _total_money < (_total_withdraw + withdraw.money):
        return CustomException(http_code=400, code='400', message='Yêu cầu vượt quá tổng số tiền')

    withdraw_db = Withdraw(user_id=current_user.id, **withdraw.dict())
    print(Withdraw)
    db.session.add(withdraw_db)
    db.session.commit()
    db.session.refresh(withdraw_db)
    return DataResponse().success_response({})


@router.post("/reply", dependencies=[Depends(PermissionRequired('admin'))])
def reply(withdraw: WithdrawReply):
    user_db = db.session.query(User).filter_by(id=withdraw.user_id).first()
    if not user_db:
        return CustomException(http_code=400, code='400', message="user not found")
    db.session.query(Withdraw).filter_by(id=withdraw.id).update(**withdraw.dict())
    db.session.commit()
    return DataResponse().success_response({})

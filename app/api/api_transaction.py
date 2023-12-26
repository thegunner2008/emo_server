from fastapi import APIRouter, Depends

from app.enum.enum_withdraw import StatusWithdraw
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import PaginationParams, paginate
from app.models import User, Withdraw
from app.models.model_transaction import Transaction
from app.models.model_job import Job

from fastapi_sqlalchemy import db
from sqlalchemy import func, and_

from app.schemas.sche_base import DataResponse
from app.services.srv_user import UserService

router = APIRouter()


@router.get("", dependencies=[Depends(login_required)])
def get_transactions(current_user: User = Depends(UserService().get_current_user),
                     params: PaginationParams = Depends()):
    current_user_id = current_user.id
    total_money = db.session.query(func.sum(Transaction.money)).filter(
        Transaction.user_id == current_user_id
    ).scalar() or 0

    total_withdraw = db.session.query(func.sum(Withdraw.money)).filter(
        Withdraw.user_id == current_user_id,
        Withdraw.status == StatusWithdraw.transferred
    ).scalar() or 0

    query_jobs = db.session.query(Transaction.id, Transaction.created_at, Transaction.money, Job).join(
        Transaction, Transaction.job_id == Job.id
    ).filter(
        Transaction.user_id == current_user_id
    )

    return {
        "total_money": total_money,
        "total_withdraw": total_withdraw,
        **paginate(Transaction, query_jobs, params).dict()
    }


@router.get("/by_time", dependencies=[Depends(login_required)])
def get_transactions_by_times(start: int, end: int, current_user: User = Depends(UserService().get_current_user)):
    current_user_id = current_user.id
    total_money = db.session.query(func.sum(Transaction.money)).filter(
        Transaction.user_id == current_user_id
    ).scalar() or 0

    total_withdraw = db.session.query(func.sum(Withdraw.money)).filter(
        Withdraw.user_id == current_user_id,
        Withdraw.status == StatusWithdraw.transferred
    ).scalar() or 0

    query_jobs = db.session.query(Transaction.id, Transaction.created_at, Transaction.money, Job).join(
        Transaction, Transaction.job_id == Job.id
    ).filter(
        and_(Transaction.time_int <= end, Transaction.time_int >= start)
    )

    return {
        "total_money": total_money,
        "total_withdraw": total_withdraw,
        "data": query_jobs.all()
    }


@router.get("/all", dependencies=[Depends(PermissionRequired('admin'))])
def get_transactions(job_id: str):
    query_jobs = db.session.query(Transaction).filter(
        Transaction.job_id == job_id
    )
    return DataResponse().success_response(data=query_jobs.all())

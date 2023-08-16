from fastapi import APIRouter, Depends

from app.enum.enum_withdraw import StatusWithdraw
from app.helpers.login_manager import login_required
from app.helpers.paging import PaginationParams, paginate
from app.models import User, Withdraw
from app.models.model_transaction import Transaction
from app.models.model_job import Job

from fastapi_sqlalchemy import db
from sqlalchemy import func

from app.services.srv_user import UserService

router = APIRouter()


@router.get("", dependencies=[Depends(login_required)])
def get_transactions(current_user: User = Depends(UserService().get_current_user),
                     params: PaginationParams = Depends()):
    current_user_id = current_user.id
    total_money = db.session.query(func.sum(Transaction.money)).filter(
        Transaction.user_id == current_user_id).scalar() or 0
    total_withdraw = db.session.query(func.sum(Withdraw.money)).filter(Withdraw.user_id == current_user_id,
                                                                       Withdraw.status == StatusWithdraw.transferred).scalar() or 0
    query_jobs = db.session.query(Job, Transaction.created_at, Transaction.money).join(Transaction, Job.id == Transaction.job_id).filter(
        Transaction.user_id == current_user_id)

    return {"total_money": total_money, "total_withdraw": total_withdraw, **paginate(Job, query_jobs, params).dict()}

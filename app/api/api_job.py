from typing import Any

from fastapi import APIRouter, Depends

from app.enum.enum_withdraw import StatusWithdraw
from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required
from app.helpers.paging import Page, PaginationParams, paginate
from app.helpers.token_job import create_token_job, decode_token_job, TokenJob
from app.models import User, Current, Withdraw
from app.models.user_job import UserJob
from app.schemas.sche_base import DataResponse
from app.schemas.sche_job import JobItemResponse, JobCreate, JobStart
from app.models.model_job import Job

from fastapi_sqlalchemy import db
from cachetools import TTLCache
from datetime import datetime, timedelta
from sqlalchemy import and_, func

from app.services.srv_job import JobService
from app.services.srv_user import UserService

router = APIRouter()
cache = TTLCache(maxsize=1000, ttl=500)
detal_time = 10


@router.get("", response_model=Page[JobItemResponse])
def get(params: PaginationParams = Depends()) -> Any:
    try:
        _query = db.session.query(Job)
        jobs = paginate(model=Job, query=_query, params=params)
        return jobs
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.post("")
def post(job: JobCreate):
    job_db = Job(**job.dict())
    db.session.add(job_db)
    db.session.commit()
    db.session.refresh(job_db)
    return job_db


@router.get("/current", dependencies=[Depends(login_required)])
def get_current(current_user: User = Depends(UserService().get_current_user)):
    return JobService().get_current_job(current_user.id)


@router.get("/start", dependencies=[Depends(login_required)])
def start(job_id: int, current_id: int, current_user: User = Depends(UserService().get_current_user)):
    job_db = db.session.query(Job).filter_by(id=job_id).first()
    user_db = db.session.query(User).filter_by(id=current_user.id).first()
    if not job_db or not user_db:
        return CustomException(http_code=400, code='400', message="job or user not found")
    current_time = datetime.now()
    cache[current_user.id] = current_time
    return DataResponse().success_response({
        "token": create_token_job(job_id=job_id, user_id=current_user.id, current_id=current_id),
        "key": job_db.key_page,
    })


@router.get("/finish")
def finish(token: str, value_page: str):
    token_job = decode_token_job(token=token)
    job_db = db.session.query(Job).filter_by(id=token_job.job_id).first()
    current_db = db.session.query(Current).filter_by(id=token_job.current_id).first()
    if not job_db or not current_db:
        return CustomException(http_code=400, code='400', message="job or current not found")
    if value_page != job_db.value_page:
        return CustomException(http_code=400, code='400', message="value page is not correct")
    if not cache.get(token_job.user_id):
        return CustomException(http_code=400, code='400', message=f"Time out")
    current_time = datetime.now()
    diff = current_time - cache.get(token_job.user_id)
    diff_int = int(diff.total_seconds())
    if not (diff_int - detal_time < job_db.time < diff_int + detal_time):
        return CustomException(http_code=400, code='400', message=f"Time out + {diff_int}")
    user_job_find = db.session.query(UserJob).filter(
        and_(UserJob.user_id == token_job.user_id, UserJob.job_id == token_job.job_id)).first()
    if user_job_find:
        return CustomException(http_code=400, code='400', message="Done before")
    user_job = UserJob(user_id=token_job.user_id, job_id=token_job.job_id)
    db.session.add(user_job)
    db.session.delete(current_db)
    db.session.commit()
    db.session.refresh(user_job)

    return DataResponse().success_response(data=user_job)


@router.get("/done", dependencies=[Depends(login_required)])
def get_job_done(current_user: User = Depends(UserService().get_current_user), params: PaginationParams = Depends()):
    current_user_id = current_user.id
    _query_total_money = db.session.query(func.sum(Job.money)).join(UserJob, Job.id == UserJob.job_id).filter(
        UserJob.user_id == current_user_id)
    _total_money = _query_total_money.scalar()

    _query_total_withdraw = db.session.query(func.sum(Withdraw.money)) \
        .filter(Withdraw.user_id == current_user_id, Withdraw.status == StatusWithdraw.transferred)
    _total_withdraw = _query_total_withdraw.scalar()

    _query_user_jobs = db.session.query(Job, UserJob.created_at).join(UserJob, Job.id == UserJob.job_id).filter(
        UserJob.user_id == current_user_id)

    return {"total_money": _total_money, "total_withdraw": _total_withdraw or 0,
            **paginate(Job, _query_user_jobs, params).dict()}

from typing import Any

from app.services.srv_google import GoogleService
from fastapi import APIRouter, Depends, Request

from app.helpers.enums import UserRole
from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate
from app.models import User, Price, Transaction
from app.schemas.sche_base import DataResponse
from app.schemas.sche_job import JobItemResponse, JobCreate, JobFinish, JobUpdate, JobCancel, JobTool, JobPrepare, \
    JobEdit
from app.models.model_job import Job

from fastapi_sqlalchemy import db

from app.services.srv_job import JobService
from app.services.srv_user import UserService

router = APIRouter()


@router.get("/current", dependencies=[Depends(login_required)])
def get_current(request: Request, device_id: str, current_user: User = Depends(UserService().get_current_user)):
    return JobService().get_current_job(request, device_id, current_user.id)


@router.get("/remain_job", dependencies=[Depends(PermissionRequired(UserRole.ADMIN.value))])
def get_remain_jobs():
    return JobService().get_remain_jobs()


@router.get("/start", dependencies=[Depends(login_required)])
def start(job_id: int, current_id: int, current_user: User = Depends(UserService().get_current_user)):
    return JobService().start(job_id=job_id, user_id=current_user.id, current_id=current_id)


@router.post("/finish_tool", dependencies=[Depends(PermissionRequired(UserRole.ADMIN.value))])
def finish(job_tools: list[JobTool]):
    res = JobService().finish_tool(job_tools)
    return DataResponse().success_response(data=res)


@router.post("/finish", dependencies=[Depends(login_required)])
def finish(request: Request, job_finish: JobFinish):
    res = JobService().finish(request, job_finish)
    return DataResponse().success_response(data=res)


@router.post("/cancel", dependencies=[Depends(login_required)])
def cancel(request: Request, job_cancel: JobCancel, current_user: User = Depends(UserService().get_current_user)):
    res = JobService().cancel(request, user_id=current_user.id, job_cancel=job_cancel)
    return DataResponse().success_response(data=res)


@router.get("", response_model=Page[JobItemResponse])
def get(params: PaginationParams = Depends()) -> Any:
    try:
        _query = db.session.query(Job)
        jobs = paginate(model=Job, query=_query, params=params)
        return jobs
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


# Admin
@router.get("/{job_id}")
def get(job_id: int):
    job_db = db.session.query(Job).get(job_id)
    if job_db:
        return DataResponse().success_response(data=job_db)
    else:
        raise CustomException(http_code=404, code='404', message="Không tìm thấy dữ liệu")


@router.post("/prepare", dependencies=[Depends(login_required)])
def post(job: JobPrepare, current_user: User = Depends(UserService().get_current_user)):
    is_admin = current_user.role == UserRole.ADMIN.value
    index = GoogleService().get_google_index(job.key_search, job.url)

    prices = db.session.query(Price).all() if is_admin else db.session.query(Price.time, Price.price).all()
    return DataResponse().success_response(data={"prices": prices, "index": index})


@router.get("/prices", dependencies=[Depends(login_required)])
def get_prices():
    return db.session.query(Price).all()


@router.post("/create", dependencies=[Depends(login_required)])
def post(job: JobCreate, current_user: User = Depends(UserService().get_current_user)):
    is_admin = current_user.role == UserRole.ADMIN.value
    job_db = Job(**job.dict())
    if not is_admin:
        prices = db.session.query(Price.time, Price.money, Price.price).all()
        price_found = False
        for price in prices:
            if price.time == job_db.time:
                job_db.money = price.money
                job_db.price = price.price
                price_found = True
                break
        if not price_found:
            raise CustomException(http_code=400, code='400', message="Không tìm thấy giá")
    if current_user.role != UserRole.ADMIN.value or not job_db.user_id:
        job_db.user_id = current_user.id
    if job_db.time > 10:
        job_db.time = 10

    db.session.add(job_db)
    db.session.commit()
    db.session.refresh(job_db)

    return DataResponse().success_response(data=job_db)


@router.put("/{job_id}", dependencies=[Depends(login_required)])
def put(job_id: int, job_edit: JobEdit, current_user: User = Depends(UserService().get_current_user)):
    is_admin = current_user.role == UserRole.ADMIN.value
    job_db = db.session.query(Job).get(job_id)
    if not job_db:
        raise CustomException(http_code=400, code='400', message="Không tìm thấy dữ liệu")
    for field, value in job_edit.dict(exclude_unset=True).items():
        setattr(job_db, field, value)
    if not is_admin:
        prices = db.session.query(Price.time, Price.money, Price.price).all()
        price_found = False
        for price in prices:
            if price.time == job_db.time:
                job_db.money = price.money
                job_db.price = price.price
                price_found = True
                break
        if not price_found:
            raise CustomException(http_code=400, code='400', message="Không tìm thấy giá")
    if current_user.role != UserRole.ADMIN.value or not job_db.user_id:
        job_db.user_id = current_user.id
    if job_db.time > 10:
        job_db.time = 10

    db.session.commit()
    db.session.refresh(job_db)

    return DataResponse().success_response(data=job_db)


@router.post("/create_list", dependencies=[Depends(login_required)])
def post(jobs: list[JobCreate], current_user: User = Depends(UserService().get_current_user)):
    is_admin = current_user.role == UserRole.ADMIN.value
    if not is_admin:
        prices = db.session.query(Price.time, Price.money, Price.price).all()
        if not prices:
            raise CustomException(http_code=400, code='400', message="Không tìm thấy giá")

    job_dbs = []
    for job in jobs:
        job_db = Job(**job.dict())
        if not is_admin and prices:
            for price in prices:
                if price.time == job_db.time:
                    job_db.money = price.money
                    job_db.price = price.price
                    break
        if current_user.role != UserRole.ADMIN.value or not job_db.user_id:
            job_db.user_id = current_user.id
        if job_db.time > 10:
            job_db.time = 10
        job_dbs.append(job_db)

    db.session.add_all(job_dbs)
    db.session.commit()
    db.session.refresh(job_dbs)

    return DataResponse().success_response(data=job_dbs)


@router.delete("")
def delete(job_id: int):
    job_db = db.session.query(Job).get(job_id)
    if job_db:
        transactions = db.session.query(Transaction).filter(Transaction.job_id == job_id).all()
        for transaction in transactions:
            db.session.delete(transaction)

        db.session.delete(job_db)
        db.session.commit()
        return DataResponse().success_response("Thành công")
    else:
        return CustomException(http_code=400, code='400', message="Không tìm thấy dữ liệu")


@router.get("/check")
def check():
    return JobService().check_status()

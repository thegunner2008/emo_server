from typing import Any

from fastapi import APIRouter, Depends, Request

from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required
from app.helpers.paging import Page, PaginationParams, paginate
from app.models import User
from app.schemas.sche_base import DataResponse
from app.schemas.sche_job import JobItemResponse, JobCreate, JobFinish, JobUpdate, JobCancel
from app.models.model_job import Job

from fastapi_sqlalchemy import db

from app.services.srv_job import JobService
from app.services.srv_user import UserService

router = APIRouter()


@router.get("/current", dependencies=[Depends(login_required)])
def get_current(request: Request, device_id: str, current_user: User = Depends(UserService().get_current_user)):
    return JobService().get_current_job(request, device_id, current_user.id)


@router.get("/start", dependencies=[Depends(login_required)])
def start(job_id: int, current_id: int, current_user: User = Depends(UserService().get_current_user)):
    return JobService().start(job_id=job_id, user_id=current_user.id, current_id=current_id)


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


@router.post("")
def post(job: JobCreate):
    job_db = Job(**job.dict())
    db.session.add(job_db)
    db.session.commit()
    db.session.refresh(job_db)
    return job_db


@router.put("/{job_id}")
def put(job_id: int, job_update: JobUpdate):
    job_db = db.session.query(Job).get(job_id)
    if job_db:
        job_data = job_update.dict(exclude_unset=True)
        for key, value in job_data.items():
            setattr(job_db, key, value)
        db.session.merge(job_db)
        db.session.commit()
        return DataResponse().success_response("Thành công")
    else:
        raise CustomException(http_code=404, code='404', message="Không tìm thấy dữ liệu")


@router.delete("")
def delete(job_id: int):
    job_db = db.session.query(Job).get(job_id)
    if job_db:
        db.session.delete(job_db)
        db.session.commit()
        return DataResponse().success_response("Thành công")
    else:
        return CustomException(http_code=400, code='400', message="Không tìm thấy dữ liệu")

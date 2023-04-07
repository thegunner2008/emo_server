from typing import Dict, Any, Union

from fastapi_sqlalchemy import db

from app.helpers.exception_handler import CustomException
from app.models import Job, Current
from app.models.user_job import UserJob
from sqlalchemy import and_

from app.redis import get_redis
from app.schemas.sche_base import DataResponse


class JobService(object):
    __instance = None

    @staticmethod
    def get_current_job(device_id: str, user_id: int) -> dict[str, Any]:
        first_current = db.session.query(Current).filter_by(user_id=user_id).first()
        if first_current:
            db.session.query(Current).filter(Current.user_id == user_id).filter(Current.id != first_current.id).delete()
            db.session.commit()
            return DataResponse().success_response(
                data={
                    "current_id": first_current.id,
                    "job": first_current.job,
                })

        if device_id:
            member_jobs_id = get_redis().smembers(device_id)
            job_ids = [int(job_id.decode('utf-8')) for job_id in member_jobs_id]
        else:
            user_jobs = db.session.query(UserJob).filter(UserJob.user_id == user_id).all()
            job_ids = list(set([user_job.job_id for user_job in user_jobs]))

        first_job = db.session.query(Job).filter(and_(Job.id.notin_(job_ids), Job.count < Job.total)).first()
        if not first_job:
            return DataResponse().success_response(data={
                "current_id": -1,
                "job": None,
            })
        current_db = Current(
            user_id=user_id,
            job_id=first_job.id
        )
        db.session.add(current_db)
        db.session.commit()
        db.session.refresh(current_db)
        get_redis().sadd(device_id, first_job.id)
        return DataResponse().success_response(data={
            "current_id": current_db.id,
            "job": current_db.job,
        })

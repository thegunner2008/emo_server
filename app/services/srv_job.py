from typing import Dict, Any

from fastapi_sqlalchemy import db

from app.helpers.exception_handler import CustomException
from app.models import Job, Current
from app.models.user_job import UserJob
from sqlalchemy import and_

from app.schemas.sche_base import DataResponse


class JobService(object):
    __instance = None

    @staticmethod
    def get_current_job(user_id: int) -> dict[str, Any] | Current:
        first_current = db.session.query(Current).filter_by(user_id=user_id).first()
        if first_current:
            db.session.query(Current).filter(Current.user_id == user_id).filter(Current.id != first_current.id).delete()
            db.session.commit()
            return DataResponse().success_response(
                data={
                    "current_id": first_current.id,
                    "job": first_current.job,
                })
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
        return DataResponse().success_response(data={
            "current_id": current_db.id,
            "job": current_db.job,
        })

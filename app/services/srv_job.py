from datetime import datetime, timedelta
from typing import Dict, Any, Union

from cachetools import TTLCache
from fastapi import Request

from fastapi_sqlalchemy import db

from app.helpers.exception_handler import CustomException
from app.helpers.time_int import time_int_short_day, time_int_short, now_int
from app.helpers.token_job import decode_token_job, create_token_job
from app.models import Job, Current, User
from app.models.model_total import Total
from app.models.model_transaction import Transaction
from sqlalchemy import and_, or_, update, select

from app.redis import set_time_redis, get_time_redis, get_redis, get_count_redis, set_count_redis
from app.schemas.sche_base import DataResponse
from app.schemas.sche_job import JobFinish, JobCancel

detal_time = 10

r = get_redis()


class JobService(object):
    __instance = None

    @staticmethod
    def check_status():
        keys = r.keys('*')
        values_dict = {}
        for key in keys:
            typ = r.type(key)
            va = None
            if typ == "string":
                va = r.get(key)
            if typ == "hash":
                va = r.hgetall(key)
            if typ == "zset":
                va = r.zrange(key, 0, -1)
            if typ == "list":
                va = r.lrange(key, 0, -1)
            if typ == "set":
                va = r.smembers(key)
            values_dict[key] = va
        return values_dict

    @staticmethod
    def get_current_job(request: Request, imei: str, user_id: int) -> dict[str, Any]:
        # Nếu có job đang làm thì trả về job đó
        try:
            first_current = db.session.query(Current).filter_by(user_id=user_id).first()
            if first_current:
                db.session.query(Current).filter(Current.user_id == user_id).filter(
                    Current.id != first_current.id).delete()
                db.session.commit()
                return DataResponse().success_response(
                    data={
                        "current_id": first_current.id,
                        "job": first_current.job,
                    })
            device_id = imei if (imei and imei != "unknown") else request.client.host

            # Lấy danh sách job đã làm trong {reset_day} ngày
            job_id_blocks = db.session.query(Transaction.job_id).filter(
                and_(Transaction.device_id == device_id, Transaction.time_int >= time_int_short_day())).distinct().all()

            job_id_blocks = set(job_id[0] for job_id in job_id_blocks)

            # Lọc job chưa làm trong {reset_day} ngày, chưa hết hạn
            jobs = db.session.query(Job).filter(
                and_(
                    Job.id.notin_(job_id_blocks),
                    or_(Job.finish_at.is_(None), Job.finish_at >= datetime.now())
                )
            ).all()

            # Lọc job đã làm < total trong ngày
            jobs = list(filter(lambda e: e.total > get_count_redis(e.id), jobs))

            if len(jobs) == 0:
                return DataResponse().success_response(data={
                    "current_id": -1,
                    "job": None,
                })
            # Chọn job có số lượng ít nhất trong ngày (* hệ số)
            min_job = min(jobs, key=lambda e: get_count_redis(e.id) * e.factor)

            current_db = Current(
                user_id=user_id,
                job_id=min_job.id
            )
            db.session.add(current_db)
            db.session.commit()
            db.session.refresh(current_db)
            return DataResponse().success_response(data={
                "current_id": current_db.id,
                "job": current_db.job,
            })
        except Exception as e:
            raise CustomException(http_code=400, code='400', message=f"error {e}")

    @staticmethod
    def start(job_id: int, user_id: int, current_id: int) -> dict[str, Any]:
        job_db = db.session.query(Job).filter_by(id=job_id).first()
        user_db = db.session.query(User).filter_by(id=user_id).first()
        if not job_db or not user_db:
            raise CustomException(http_code=400, code='400', message="job or user not found")
        set_time_redis(user_id=user_id)
        return DataResponse().success_response({
            "token": create_token_job(job_id=job_id, user_id=user_id, current_id=current_id),
            "key": job_db.key_page,
        })

    @staticmethod
    def finish(request: Request, job_finish: JobFinish) -> dict[str, Any]:
        token_job = decode_token_job(token=job_finish.token)
        job_db = db.session.query(Job).filter_by(id=token_job.job_id).first()
        current_db = db.session.query(Current).filter_by(id=token_job.current_id).first()

        if not job_db or not current_db:
            error = "job or current not found"
        elif job_finish.value_page != job_db.value_page or job_db.value_page is None:
            error = "value page is not correct"
        elif check_time_out(user_id=token_job.user_id, job_time=job_db.time):
            error = "Time out"
        else:
            error = None
        if error:
            raise CustomException(http_code=400, code='400', message=error)

        transaction = Transaction(user_id=token_job.user_id, job_id=token_job.job_id, ip=request.client.host,
                                  device_id=job_finish.imei, money=job_db.money,
                                  time_int=time_int_short(reset_day=job_db.reset_day))
        db.session.add(transaction)
        db.session.delete(current_db)
        db.session.commit()
        db.session.refresh(transaction)

        transactions = db.session.query(Transaction).filter_by(user_id=token_job.user_id).all()
        qr = update(Job).where(Job.id == transaction.job_id).values(count=Job.count + 1)
        db.session.execute(qr)
        qr1 = update(Total).where(Total.user_id == token_job.user_id) \
            .values(count_transaction=transactions.__len__(), total=sum(int(e.money) for e in transactions),
                    count_job=set(e.job_id for e in transactions).__len__())
        db.session.execute(qr1)
        db.session.commit()
        set_count_redis(job_id=token_job.job_id)
        return DataResponse().success_response(data={})

    @staticmethod
    def cancel(request: Request, user_id: int, job_cancel: JobCancel) -> dict[str, Any]:
        current_db = db.session.query(Current).filter_by(user_id=user_id).first()
        if current_db:
            db.session.delete(current_db)
        transaction = Transaction(user_id=user_id, job_id=current_db.job_id, ip=request.client.host,
                                  device_id=job_cancel.imei, money=0)
        db.session.add(transaction)
        db.session.commit()

        return DataResponse().success_response({})


def check_time_out(user_id: int, job_time: int) -> bool:
    if not get_time_redis(user_id):
        return True
    current_time = now_int()
    diff = current_time - get_time_redis(user_id)
    return not (diff - detal_time < job_time < diff + detal_time)

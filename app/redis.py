import redis

from app.core.config import settings
from app.helpers.time_int import time_int_day, now_int

r = None

TIME = "time"
COUNT = "count"


def get_redis():
    redis_host = settings.REDIS_HOST
    redis_port = settings.REDIS_PORT
    redis_password = None
    return redis.Redis(host=redis_host, port=redis_port, password=redis_password)


def set_time_redis(user_id):
    global r
    if r is None:
        r = get_redis()
    current_time = now_int()
    r.set(f"{TIME}_{user_id}", current_time)


def get_time_redis(user_id):
    global r
    if r is None:
        r = get_redis()
    return int(r.get(f"{TIME}_{user_id}"))


def set_count_redis(job_id):
    global r
    if r is None:
        r = get_redis()
    value = r.hget(COUNT, job_id)
    day_int = time_int_day()
    if value is None:
        r.set(f"{COUNT}_{job_id}", f'{day_int}_1')
    else:
        day_int_value = value.split('_')[0]
        count_value = value.split('_')[1]
        if day_int_value == day_int:
            r.set(f"{COUNT}_{job_id}", f'{day_int}_{int(count_value) + 1}')
        else:
            r.set(f"{COUNT}_{job_id}", f'{day_int}_1')


def get_count_redis(job_id):
    global r
    if r is None:
        r = get_redis()
    value = r.get(f"{COUNT}_{job_id}")
    if value is None:
        return 0
    try:
        value = value.decode('utf-8')
    finally:
        value = str(value)

    day_int_value = int(value.split('_')[0])
    count_value = int(value.split('_')[1])
    if day_int_value == time_int_day():
        return count_value
    else:
        return 0

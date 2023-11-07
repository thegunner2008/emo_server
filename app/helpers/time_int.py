from datetime import datetime, timedelta
import time


def now_int():
    return int(time.mktime(datetime.now().timetuple()))


def time_int_short(reset_day: int, dt: datetime = None):
    new_dt = dt or datetime.now()
    return int(new_dt.strftime("%Y%m%d%H")) + (reset_day - 1) * 100


def time_int_short_day(dt: datetime = None):
    new_dt = dt or datetime.now()
    return int(new_dt.strftime("%Y%m%d")) * 100


def time_int_day(dt: datetime = None):
    new_dt = dt or datetime.now()
    return int(new_dt.strftime("%Y%m%d"))


def add_time(start: datetime, delta_time: timedelta):
    return int(time.mktime((start + delta_time).timetuple()))


def delta_time_int(delta_time: timedelta):
    return int(delta_time.total_seconds())

from datetime import datetime, timedelta
import time


def now_int():
    return int(time.mktime(datetime.now().timetuple()))


def time_int_short(dt: datetime = datetime.now()):
    return int(dt.strftime("%Y%m%d%H"))


def time_int_short_day(dt: datetime = datetime.now()):
    return int(dt.strftime("%Y%m%d")) * 100


def add_time(start: datetime, delta_time: timedelta):
    return int(time.mktime((start + delta_time).timetuple()))


def delta_time_int(delta_time: timedelta):
    return int(delta_time.total_seconds())

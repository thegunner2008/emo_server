from datetime import datetime, timedelta
import time


def now_int():
    return int(time.mktime(datetime.now().timetuple()))


def add_time(start: datetime, delta_time: timedelta):
    return int(time.mktime((start + delta_time).timetuple()))


def delta_time_int(delta_time: timedelta):
    return int(delta_time.total_seconds())

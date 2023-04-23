from datetime import datetime, timedelta
import time


def now_int():
    return int(time.mktime(datetime.now().timetuple()))


def add_time(start: datetime, delta_time: timedelta):
    return int(time.mktime((start + delta_time).timetuple()))

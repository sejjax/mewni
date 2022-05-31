from typing import Callable
import schedule
from dataclasses import dataclass
from typing import Optional, Union
from functools import wraps
from .constants import MUNI_META
from .types import MuniCallbackMeta, MuniCommand, MuniScheduler
from .utils.muni_meta import set_muni_meta
from .utils.lambda_value import lambda_value
# make command


def command(name: Optional[str] = None, description: Optional[str] = None):
    def decorate(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        set_muni_meta(wrapper, MuniCommand(name if name is str else func.__name__, description))
        return wrapper
    return decorate



# WeekDay definition
@dataclass
class Day:
    number: int


DAY = Day(0)
MONDAY = Day(1)
TUESDAY = Day(2)
WEDNESDAY = Day(3)
THURSDAY = Day(4)
FRIDAY = Day(5)
SATURDAY = Day(6)
SUNDAY = Day(7)


# Usage
# @every(MONDAY, TUESDAY, at='10:20')
# def send_notification():
#   pass
def every(*kwargs, at: Optional[str] = None):
    def decorate(func: Callable):
        def wrapper():
            day_map = {
                DAY: 'day',
                MONDAY: 'monday',
                TUESDAY: 'tuesday',
                WEDNESDAY: 'wednesday',
                THURSDAY: 'thursday',
                FRIDAY: 'friday',
                SATURDAY: 'saturday',
                SUNDAY: 'sunday'
            }
            listed_args = list(kwargs)
            days: list[Day] = list(filter(lambda item: isinstance(Day, item), listed_args))
            time = at
            prepare_job = schedule.every()
            for day in days:
                day = day_map[day]
                prepare_job = getattr(prepare_job, day)
            if time is not None and time != '':
                prepare_job = prepare_job.at(time)
            job = prepare_job.do(func)
            return job
        set_muni_meta(wrapper, MuniScheduler())
        return wrapper
    return decorate




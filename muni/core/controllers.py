from typing import Callable
from enum import Enum
from functools import wraps

import aioschedule as schedule

from .types import MuniCommand, MuniScheduler
from .utils.muni_meta import set_muni_meta
from .utils.is_async import is_async


def command(name: str | None = None, description: str = 'Placeholder description'):
    def decorate(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if is_async(func):
                await func()
            else:
                func()

        set_muni_meta(wrapper, MuniCommand(name if name is str else func.__name__, description))
        return wrapper

    if callable(name):
        return decorate(name)
    return decorate


# WeekDay definition
class TimeType(Enum):
    DAY = 0


SECOND = (TimeType.DAY, -1)

DAY = (TimeType.DAY, 0)
MONDAY = (TimeType.DAY, 1)
TUESDAY = (TimeType.DAY, 2)
WEDNESDAY = (TimeType.DAY, 3)
THURSDAY = (TimeType.DAY, 4)
FRIDAY = (TimeType.DAY, 5)
SATURDAY = (TimeType.DAY, 6)
SUNDAY = (TimeType.DAY, 7)


# Usage
# @every(MONDAY, TUESDAY, at='10:20')
# def send_notification():
#   pass
def every(*kwargs, at: str | None = None):
    def decorate(func: Callable):
        @wraps(func)
        def wrapper():
            day_map = {
                SECOND: 'second',
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
            days: list = list(filter(lambda item: item[0] == TimeType.DAY, listed_args))
            time = at
            prepare_job = schedule.every()
            for day in days:
                day = day_map[day]
                prepare_job = getattr(prepare_job, day)
            if time is not None and time != '':
                if len(days) == 0:
                    prepare_job = prepare_job.day.at(time)
                else:
                    prepare_job = prepare_job.at(time)

            async def async_func():
                if is_async(func):
                    return await func()
                func()

            job = prepare_job.do(async_func)
            return job

        set_muni_meta(wrapper, MuniScheduler())
        return wrapper

    return decorate

from datetime import datetime
from typing import NamedTuple


Timestump = str
Timezone = str


class Daytime(NamedTuple):
    day: int
    month: int
    year: int
    timestamp: Timestump
    time_zone: Timezone


def now() -> Daytime:
    now = datetime.now()
    now_with_tz = now.astimezone()
    my_timezone = now_with_tz.tzinfo
    return Daytime(
        day=now_with_tz.day,
        month=now_with_tz.month,
        year=now_with_tz.year,
        timestamp=f'{now_with_tz}',
        time_zone=f'{my_timezone}'
    )

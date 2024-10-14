from datetime import datetime
from typeguard import typechecked
import pytz

TIMEZONE = 'Europe/Helsinki'


@typechecked
def to_utc_date(date: datetime) -> datetime:
    return date.replace(tzinfo=pytz.UTC)

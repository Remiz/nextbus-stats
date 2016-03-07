import time
import pytz
from datetime import datetime


def is_valid_time_format(time_str):
    ''' Validate a time, ex: 4:00am '''
    try:
        time.strptime(time_str, '%I:%M%p')
        return True
    except:
        return False


def timestr_to_utc(time_str, timezone):
    ''' Convert a time, ex: 4:00am to a UTC datetime object '''
    datetime_obj = datetime.strptime(time_str, '%I:%M%p')
    tz = pytz.timezone(timezone)
    datetime_obj = tz.localize(datetime_obj)
    datetime_obj = datetime_obj.astimezone(pytz.UTC)
    return datetime_obj

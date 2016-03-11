from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
import time


def is_valid_time_format(time_str):
    ''' Validate a time, ex: 23:00 '''
    try:
        time.strptime(time_str, '%H:%M')
        return True
    except:
        return False


class DateTimeTimeTransform(models.Transform):
    ''' Filter by time, thanks to charettes:
    https://www.reddit.com/r/django/comments/49p8dg/excluding_hours_range_ex_from_215am_to_5am_from_a/d0ubvls '''
    lookup_name = 'time'

    @cached_property
    def output_field(self):
        return models.TimeField()

    def as_mysql(self, compiler, connection):
        lhs, lhs_params = compiler.compile(self.lhs)
        if settings.USE_TZ:
            lhs = "CONVERT_TZ(%s, 'UTC', %%s)" % lhs
            tzname = timezone.get_current_timezone_name()
            lhs_params.append(tzname)
        sql = "TIME(%s)" % lhs
        return sql, lhs_params

    def as_postgresql(self, compiler, connection):
        lhs, lhs_params = compiler.compile(self.lhs)
        if settings.USE_TZ:
            lhs = "%s AT TIME ZONE %%s" % lhs
            tzname = timezone.get_current_timezone_name()
            lhs_params.append(tzname)
        sql = "(%s)::time" % lhs
        return sql, lhs_params

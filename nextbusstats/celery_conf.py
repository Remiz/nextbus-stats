from __future__ import absolute_import
from celery.schedules import crontab


BROKER_URL = 'redis://localhost:6379/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_SEND_TASK_ERROR_EMAILS = True
# Auto-execute celery task instead of working async (dev only)
#CELERY_ALWAYS_EAGER = True
#CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

CELERYBEAT_SCHEDULE = {
    # Collect stop predictions
    'collect-prediction': {
        'task': 'nextbusstats.routes.tasks.collect_predictions',
        'schedule': crontab(minute='*/1'),
        'args': ()
    }
}

CELERY_TIMEZONE = 'America/Toronto'

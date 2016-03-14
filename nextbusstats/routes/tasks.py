from celery import task
from django.conf import settings
from django.core.paginator import Paginator
from nextbusstats.nextbus.api_utils import NextBus
from .models import Route, Stop, Prediction


@task()
def collect_predictions():
    """Retrieve predictions for the routes that are monitored
    Be aware of NextBus API rate limits:
      - 2MB/20sec,
      - 150 stops per prediction
    """
    nb = NextBus()
    monitored_routes = Route.objects.filter(monitored=True)
    for route in monitored_routes:
        all_stops = route.stops.all()
        p = Paginator(all_stops, 150)  # Paginate routes with more than 150 stops
        for page_number in p.page_range:
            page = p.page(page_number)
            stops = page.object_list
            stop_tags = ['%s|%s' % (stop.route.tag, stop.tag) for stop in stops]
            predictions = nb.get_first_prediction_multi_stops(settings.AGENCY_TAG, stop_tags)
            for prediction in predictions:
                new_prediction = Prediction(
                    seconds=prediction[1],
                    stop=Stop.objects.filter(tag=prediction[0]).first()
                )
                new_prediction.save()

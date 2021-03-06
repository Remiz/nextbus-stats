import pytz
import json
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Avg
from django.db import models
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import ensure_csrf_cookie
from nextbusstats.common.tools import is_valid_time_format, DateTimeTimeTransform
from .models import Route, Direction, Stop, Prediction

# allows filtering by __time
models.DateTimeField.register_lookup(DateTimeTimeTransform)


def routes_list(request):
    return render(request, 'routes/routes_list.html', {
        'routes': Route.objects.filter(monitored=True),
    })


@ensure_csrf_cookie
def route(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    return render(request, 'routes/route.html', {
        'route': route,
    })


def get_chart(request):
    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseForbidden()
    stop_id = request.POST.get('stop_id', None)
    if stop_id in [None, '']:
        raise ValueError("stop_id can't be None or empty")
    stop = get_object_or_404(Stop, pk=stop_id)
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    frequency = request.POST.get('frequency', '1t')
    time_start = request.POST.get('time_start')
    time_end = request.POST.get('time_end')
    tzname = request.POST.get('timezone', 'America/Toronto')
    timezone.activate(pytz.timezone(tzname))
    predictions = Prediction.objects.filter(
        stop=stop,
        posted_at__gt=date_from,
        posted_at__lte=date_to,
    )
    if is_valid_time_format(time_start) and is_valid_time_format(time_end):
        predictions = predictions.exclude(posted_at__time__range=(time_end, time_start))
    # Converting predictions to Pandas timeseries and resample by frequency
    dataframe = predictions.to_timeseries(
        fieldnames=['posted_at', 'seconds'],
        index='posted_at',
        values='seconds',
        freq=frequency,  # resampling triggers deprecation warning to use .mean()
    ).dropna(how='any')  # Drop nan
    predictions_json = dataframe.to_json(date_format='iso', orient='index')
    return HttpResponse(predictions_json, content_type='application/json')


def get_daily_average_chart(request):
    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseForbidden()
    stop_id = request.POST.get('stop_id', None)
    if stop_id in [None, '']:
        raise ValueError("stop_id can't be None or empty")
    stop = get_object_or_404(Stop, pk=stop_id)
    time_start = request.POST.get('time_start')
    time_end = request.POST.get('time_end')
    tzname = request.POST.get('timezone', 'America/Toronto')
    timezone.activate(pytz.timezone(tzname))
    avg_weekday = {}
    for weekday in range(1, 8):
        prediction_avg = Prediction.objects.filter(
            stop=stop,
            posted_at__week_day=weekday
        )
        if is_valid_time_format(time_start) and is_valid_time_format(time_end):
            prediction_avg = prediction_avg.exclude(posted_at__time__range=(time_end, time_start))
        prediction_avg = prediction_avg.aggregate(Avg('seconds'))
        avg_weekday[weekday] = prediction_avg['seconds__avg']
    response = {'avg_weekday': avg_weekday}
    return HttpResponse(json.dumps(response), content_type='application/json')


def get_hourly_average_chart(request):
    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseForbidden()
    stop_id = request.POST.get('stop_id', None)
    if stop_id in [None, '']:
        raise ValueError("stop_id can't be None or empty")
    stop = get_object_or_404(Stop, pk=stop_id)
    time_start = request.POST.get('time_start')
    time_end = request.POST.get('time_end')
    tzname = request.POST.get('timezone', 'America/Toronto')
    timezone.activate(pytz.timezone(tzname))
    avg_hourly = {}
    for hour in range(0, 24):
        prediction_avg = Prediction.objects.filter(
            stop=stop,
            posted_at__hour=hour
        )
        if is_valid_time_format(time_start) and is_valid_time_format(time_end):
            prediction_avg = prediction_avg.exclude(posted_at__time__range=(time_end, time_start))
        prediction_avg = prediction_avg.aggregate(Avg('seconds'))
        avg_hourly[hour] = prediction_avg['seconds__avg']
    response = {'avg_hourly': avg_hourly}
    return HttpResponse(json.dumps(response), content_type='application/json')


def get_stops_from_direction(request):
    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseForbidden()
    direction_id = request.POST.get('direction', None)
    if direction_id in [None, '']:
        raise ValueError("direction_id can't be None or empty")
    direction = get_object_or_404(Direction, pk=direction_id)
    stops = []
    for stop in direction.stops.all().order_by('directionstop__position'):
        stops.append({
            'id': stop.id,
            'title': stop.title,
        })
    response = {'stops': stops}
    return HttpResponse(json.dumps(response), content_type='application/json')

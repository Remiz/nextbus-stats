from django.shortcuts import render, get_object_or_404
from django_ajax.decorators import ajax
from django.http import Http404
from .models import Route, Direction, Stop, Prediction


def routes_list(request):
    return render(request, 'routes/routes_list.html', {
        'routes': Route.objects.filter(monitored=True),
    })


def route(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    return render(request, 'routes/route.html', {
        'route': route,
    })


@ajax
def get_chart(request):
    if request.method != 'POST':
        raise Http404
    stop = get_object_or_404(Stop, pk=request.POST.get('stop_selected', None))
    datetime_from = request.POST.get('datetime_from')
    print datetime_from
    datetime_to = request.POST.get('datetime_to')
    predictions = Prediction.objects.filter(
        stop=stop,
        posted_at__gt=datetime_from,
        posted_at__lte=datetime_to,
    )
    formated_predictions = []
    for prediction in predictions:
        formated_predictions.append({
            'posted_at': prediction.posted_at.isoformat(),
            'prediction': prediction.seconds,
        })
    return {'predictions': formated_predictions}


@ajax
def get_stops_from_direction(request):
    if request.method != 'POST':
        raise Http404
    direction = get_object_or_404(Direction, pk=request.POST.get('direction', None))
    stops = []
    for stop in direction.stops.all().order_by('directionstop__position'):
        stops.append({
            'id': stop.id,
            'title': stop.title,
        })
    return {'stops': stops}

import factory
from datetime import timedelta
from django.utils import timezone
from factory import fuzzy
from .models import (
    Route, Direction, Stop, DirectionStop, Prediction
)


class RouteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Route

    tag = '123'
    title = 'Bus 123'
    color = '000FFF'
    opposite_color = 'FFFFFF'
    lat_min = 0
    lat_max = 0
    lon_min = 0
    lon_max = 0
    monitored = True


class DirectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Direction

    tag = '123_south'
    title = 'Bus 123 Southbound'
    name = 'Bus 123 Southbound'
    route = factory.SubFactory(RouteFactory)


class StopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stop

    tag = '10_main_st'
    stop_id = 12345
    title = '10 Main St. West'
    lat = 0
    lon = 0
    route = factory.SubFactory(RouteFactory)


class DirectionStopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DirectionStop

    direction = factory.SubFactory(DirectionFactory)
    stop = factory.SubFactory(StopFactory)
    position = 1


class DirectionWithStopFactory(DirectionFactory):
    membership = factory.RelatedFactory(DirectionStopFactory, 'direction')


class DirectionWith2StopsFactory(DirectionFactory):
    membership1 = factory.RelatedFactory(DirectionStopFactory, stop__title='Stop1')
    membership2 = factory.RelatedFactory(DirectionStopFactory, stop__title='Stop2')


class PredictionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Prediction

    posted_at = fuzzy.FuzzyDateTime(timezone.now() - timedelta(hours=1))
    seconds = fuzzy.FuzzyInteger(1, 500)
    stop = factory.SubFactory(StopFactory)

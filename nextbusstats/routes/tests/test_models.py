from django.test import TestCase
from nextbusstats.routes.factories import (
    RouteFactory, StopFactory, DirectionFactory, DirectionStopFactory,
    PredictionFactory
)


class RoutesModelsTest(TestCase):

    def test_route_create(self):
        route_1 = RouteFactory(
            title='Route 1'
        )

    def test_direction_create(self):
        route_1 = RouteFactory()
        direction_1 = DirectionFactory(
            title='Direction 1',
            route=route_1
        )

    def test_stops_create(self):
        route_1 = RouteFactory(
            title='Route 1',
        )
        direction_1 = DirectionFactory(
            title='Direction 1',
            route=route_1
        )
        for i in range(0, 10):
            stop = StopFactory(
                title='Stop %s' % i,
                route=route_1
            )
            direction_stop = DirectionStopFactory(
                direction=direction_1,
                stop=stop,
                position=i
            )
        self.assertEqual(direction_1.stops.count(), 10)

    def test_prediction_create(self):
        prediction_1 = PredictionFactory()
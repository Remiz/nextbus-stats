import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from nextbusstats.routes.factories import (
    RouteFactory, DirectionFactory, PredictionFactory,
    StopFactory, DirectionStopFactory
)


class RoutesViewsTest(TestCase):

    def setUp(self):
        self.route_1 = RouteFactory()
        self.direction_1 = DirectionFactory(
            title='Direction 1',
            route=self.route_1
        )
        self.direction_2 = DirectionFactory(
            title='Direction 2',
            route=self.route_1
        )
        self.stop = StopFactory(
            route=self.route_1,
        )
        DirectionStopFactory(
            direction=self.direction_1,
            stop=self.stop,
            position=0,
        )
        for i in range(0, 10):
            prediction = PredictionFactory(
                stop=self.stop
            )

    def test_routes_list(self):
        response = self.client.get(
            reverse('routes_list')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'routes/routes_list.html')
        self.assertEqual(len(response.context['routes']), 1)

    def test_route(self):
        response = self.client.get(
            reverse('route', args=[self.route_1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'routes/route.html')
        self.assertEqual(response.context['route'].directions.count(), 2)

    def test_get_chart(self):
        # non-ajax call
        response = self.client.get(
            reverse('get_chart')
        )
        self.assertEqual(response.status_code, 403)
        # non POST call
        response = self.client.get(
            reverse('get_chart'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 403)
        # Invalid stop_id
        with self.assertRaises(ValueError):
            response = self.client.post(
                reverse('get_chart'),
                {'stop_selected': ''},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        # Get predictions

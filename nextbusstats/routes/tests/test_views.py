import json
from datetime import timedelta
from django.utils import timezone
from django.test import TestCase, Client
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
        test_ajax_post_required(self, 'get_daily_average_chart')
        # Invalid stop_id
        with self.assertRaises(ValueError):
            response = self.client.post(
                reverse('get_chart'),
                {'stop_selected': ''},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        # Get predictions
        response = self.client.post(
            reverse('get_chart'),
            {
                'stop_selected': self.stop.id,
                'datetime_from': (timezone.now() - timedelta(hours=2)).isoformat(),
                'datetime_to': timezone.now().isoformat(),
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(len(response.json()['predictions']) > 0)

    def test_get_daily_average_chart(self):
        test_ajax_post_required(self, 'get_daily_average_chart')
        # Invalid stop_id
        with self.assertRaises(ValueError):
            response = self.client.post(
                reverse('get_daily_average_chart'),
                {'stop_selected': ''},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        # Get daily average
        response = self.client.post(
            reverse('get_daily_average_chart'),
            {
                'stop_selected': self.stop.id,
                'datetime_from': (timezone.now() - timedelta(hours=2)).isoformat(),
                'datetime_to': timezone.now().isoformat(),
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(len(response.json()['avg_weekday']), 7)

    def test_get_hourly_average_chart(self):
        test_ajax_post_required(self, 'get_hourly_average_chart')
        # Invalid stop_id
        with self.assertRaises(ValueError):
            response = self.client.post(
                reverse('get_hourly_average_chart'),
                {'stop_selected': ''},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        # Get daily average
        response = self.client.post(
            reverse('get_hourly_average_chart'),
            {
                'stop_selected': self.stop.id,
                'datetime_from': (timezone.now() - timedelta(hours=2)).isoformat(),
                'datetime_to': timezone.now().isoformat(),
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(len(response.json()['avg_hourly']), 24)


def test_ajax_post_required(test_instance, view_name):
    """ Reusable set of tests to guarantee that request is Ajax POST """
    # non-ajax call
    response = test_instance.client.get(
        reverse(view_name)
    )
    test_instance.assertEqual(response.status_code, 403)
    # non POST call
    response = test_instance.client.get(
        reverse(view_name),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    test_instance.assertEqual(response.status_code, 403)

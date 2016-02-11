import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from nextbusstats.routes.factories import (
    RouteFactory, DirectionFactory
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
        self.assertEqual(response.status_code, 400)
        # non POST call
        response = self.client.get(
            reverse('get_chart'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        # response is always 200, JSON embed the status
        json_response = json.loads(response.content)
        self.assertEqual(json_response['status'], 404)
        # Invalid stop_id
        response = self.client.post(
            reverse('get_chart'),
            {'stop_selected': ''},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(json_response['status'], 500)



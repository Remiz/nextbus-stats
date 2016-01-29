from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.routes_list, name='routes_list'),
    url(r'^(?P<route_id>[0-9]+)/$', views.route, name='route'),
    url(r'^get-chart/$', views.get_chart, name='get_chart'),
    url(r'^get-stops-from-direction/$', views.get_stops_from_direction, name='get_stops_from_direction'),
]

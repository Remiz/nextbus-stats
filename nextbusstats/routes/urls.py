from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.routes_list, name='routes_list'),
    url(r'^(?P<route_id>[0-9]+)/$', views.route, name='route'),
]

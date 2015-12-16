# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-15 21:32
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings
from nextbusstats.nextbus.api_utils import NextBus


def collect_routes_and_stops(apps, schema_editor):
    """Collecting all routes and stops for a predefined agency set in Settings"""
    Route = apps.get_model('routes', 'Route')
    Stop = apps.get_model('routes', 'Stop')

    nb = NextBus()
    for route_info in nb.get_route_list(settings.AGENCY_TAG):
        route_config = nb.get_route_config(settings.AGENCY_TAG, route_info['tag'])
        route_attributes = route_config['route_attributes']
        route = Route(
            tag=route_attributes['tag'],
            title=route_attributes['title'],
            color=route_attributes['color'],
            opposite_color=route_attributes['oppositeColor'],
            lat_min=route_attributes['latMin'],
            lat_max=route_attributes['latMax'],
            lon_min=route_attributes['lonMin'],
            lon_max=route_attributes['lonMax'],
        )
        route.save()
        for stop_info in route_config['stops']:
            if 'stopId' in stop_info:  # stopId can be absent from stop
                stop_id = stop_info['stopId']
            else:
                stop_id = None
            stop = Stop(
                tag=stop_info['tag'],
                stop_id=stop_id,
                title=stop_info['title'],
                lat=stop_info['lat'],
                lon=stop_info['lon'],
                route=route,
            )
            stop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(collect_routes_and_stops)
    ]
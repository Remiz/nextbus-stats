from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from nextbusstats.nextbus.api_utils import NextBus
from nextbusstats.routes.models import Route, Direction, Stop, DirectionStop


class Command(BaseCommand):
    help = 'Load all the routes from the agency specified in settings'

    def handle(self, *args, **options):
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

            for direction_info in route_config['directions']:
                direction = Direction(
                    name=direction_info['name'],
                    title=direction_info['title'],
                    tag=direction_info['tag'],
                    route=route,
                )
                direction.save()

                # Saving stops order
                position = 0
                for stop_tag in direction_info['stops']:
                    direction_stop = DirectionStop(
                        direction=direction,
                        stop=Stop.objects.filter(tag=stop_tag).first(),
                        position=position
                    )
                    direction_stop.save()
                    position += 1

            self.stdout.write("Loading route: %s" % route.title)

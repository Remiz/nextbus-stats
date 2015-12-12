import requests
import xml.etree.ElementTree as ET


class NextBus():
    """Set of functions to retrieve info from NextBus api"""
    api_feed_url = 'http://webservices.nextbus.com/service/publicXMLFeed?'

    def __call_api(self, command, parameters={}):
        params_string = ''
        for param, value in parameters.iteritems():
            params_string += '&%s=%s' % (param, value)
        response = requests.get(
            self.api_feed_url+'command='+command+params_string)
        if response.status_code == 200:
            response_xml = response.text
        else:
            response.raise_for_status()
        return ET.fromstring(response_xml)

    def get_agency_list(self):
        root = self.__call_api('agencyList')
        agencies = []
        for agency in root.findall('agency'):
            agencies.append(agency.attrib)
        return agencies

    def get_route_list(self, agency_tag):
        root = self.__call_api('routeList', {'a': agency_tag})
        routes = []
        for route in root.findall('route'):
            routes.append(route.attrib)
        return routes

    def get_route_config(self, agency_tag, route_tag):
        root = self.__call_api('routeConfig', {
            'a': agency_tag,
            'r': route_tag
        })
        stops = []
        for stop in root.findall('route/stop'):
            stops.append(stop.attrib)
        directions = []
        for direction_node in root.findall('route/direction'):
            direction = direction_node.attrib
            direction_stops = []
            for stop in direction_node.findall('stop'):
                direction_stops.append(stop.attrib['tag'])
            direction['stops'] = direction_stops
            directions.append(direction)
        paths = []
        for path_node in root.findall('route/path'):
            path = []
            for point in path_node.findall('point'):
                path.append(point.attrib)
            paths.append(path)
        return {
            'route_attributes': root.find('route').attrib,
            'stops': stops,
            'directions': directions,
            'paths': paths,
        }

    def get_predictions(self, agency_tag, route_tag, stop_tag):
        root = self.__call_api('predictions', {
            'a': agency_tag,
            'r': route_tag,
            's': stop_tag,
        })
        predictions = []
        for prediction in root.findall('predictions/direction/prediction'):
            predictions.append(prediction.attrib)
        return predictions

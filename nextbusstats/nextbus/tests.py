from django.test import TestCase
from httmock import all_requests, HTTMock
from nextbusstats.nextbus.api_utils import NextBus


@all_requests
def nextbus_agency_list_mock(url, request):
    xml_response = (
        '<?xml version="1.0" encoding="utf-8" ?>',
        '<body copyright="All data copyright agencies listed below and NextBus Inc 2016.">',
        '<agency tag="portland-sc" title="Portland Streetcar" regionTitle="Oregon"/>',
        '<agency tag="sf-muni" title="San Francisco Muni" shortTitle="SF Muni" regionTitle="California-Northern"/>',
        '</body>'
    )
    return ''.join(xml_response)


@all_requests
def nextbus_route_list_mock(url, request):
    xml_response = (
        '<?xml version="1.0" encoding="utf-8" ?>',
        '<body copyright="All data copyright Toronto Transit Commission 2016.">',
        '<route tag="5" title="5-Avenue Rd"/>',
        '<route tag="6" title="6-Bay"/>',
        '<route tag="7" title="7-Bathurst"/>',
        '<route tag="8" title="8-Broadview"/>',
        '<route tag="9" title="9-Bellamy"/>',
        '<route tag="10" title="10-Van Horne"/>',
        '</body>',
    )
    return ''.join(xml_response)


class TestNextbusApiUtils(TestCase):

    def test_get_agency_list(self):
        with HTTMock(nextbus_agency_list_mock):
            nb = NextBus()
            agencies = nb.get_agency_list()
            self.assertEqual(len(agencies), 2)

    def test_get_route_list(self):
        with HTTMock(nextbus_route_list_mock):
            nb = NextBus()
            routes = nb.get_route_list('ttc')
            self.assertEqual(len(routes), 6)

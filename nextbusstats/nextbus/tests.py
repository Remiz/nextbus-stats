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


@all_requests
def nextbus_route_config_mock(url, request):
    xml_response = (
        '<?xml version="1.0" encoding="utf-8" ?>',
        '<body copyright="All data copyright Toronto Transit Commission 2016.">',
        '<route tag="512" title="512-St Clair" color="ff0000" oppositeColor="ffffff" latMin="43.6718099" latMax="43.6879999" lonMin="-79.47144" lonMax="-79.39223">',
        '<stop tag="14688" title="Gunns Loop At St Clair Ave West" lat="43.6719499" lon="-79.47144" stopId="14958"/>',
        '<stop tag="14838" title="St Clair Ave West At Old Stock Yards Rd" lat="43.6718099" lon="-79.4706" stopId="15050"/>',
        '<stop tag="14674" title="St Clair Ave West At Keele/Weston" lat="43.6724399" lon="-79.46783" stopId="14939"/>',
        '<stop tag="14295_ar" title="St Clair Station" lat="43.6877499" lon="-79.39223"/>',
        '<stop tag="14295" title="St Clair Station" lat="43.6877499" lon="-79.39223" stopId="14778"/>',
        '<stop tag="14688_ar" title="Gunns Loop At St Clair Ave West" lat="43.6719499" lon="-79.47144"/>',
        '<direction tag="512_1_512" title="West - 512 St Clair towards Keele" name="West" useForUI="true" branch="512">',
        '<stop tag="14295" />',
        '<stop tag="14688_ar" />',
        '</direction>',
        '<direction tag="512_0_512" title="East - 512 St Clair towards St Clair Station" name="East" useForUI="true" branch="512">',
        '<stop tag="14688" />',
        '<stop tag="14838" />',
        '<stop tag="14674" />',
        '<stop tag="14295_ar" />',
        '</direction>',
        '<path>',
        '<point lat="43.68462" lon="-79.41544"/>',
        '<point lat="43.68479" lon="-79.41521"/>',
        '<point lat="43.68442" lon="-79.41503"/>',
        '</path>',
        '</route>',
        '</body>',
    )
    return ''.join(xml_response)


@all_requests
def nextbus_predictions_mock(url, request):
    xml_response = (
        '<?xml version="1.0" encoding="utf-8" ?>',
        '<body copyright="All data copyright Toronto Transit Commission 2016.">',
        '<predictions agencyTitle="Toronto Transit Commission" routeTitle="512-St Clair" routeTag="512" stopTitle="St Clair Station" stopTag="14295">',
        '<direction title="East - 512 St Clair towards St Clair Station">',
        '<prediction epochTime="1456783573947" seconds="8" minutes="0" isDeparture="false" branch="512" dirTag="512_0_512" vehicle="4189" block="512_9_130" tripTag="30522435" />',
        '<prediction epochTime="1456783632023" seconds="66" minutes="1" isDeparture="false" branch="512" dirTag="512_0_512" vehicle="4150" block="512_20_142" tripTag="30522436" />',
        '<prediction epochTime="1456783740152" seconds="174" minutes="2" isDeparture="false" branch="512" dirTag="512_0_512" vehicle="4143" block="512_21_152" tripTag="30522437" />',
        '<prediction epochTime="1456783760354" seconds="194" minutes="3" isDeparture="false" branch="512" dirTag="512_0_512" vehicle="4071" block="512_10_160" tripTag="30522438" />',
        '<prediction epochTime="1456784018722" seconds="453" minutes="7" isDeparture="false" branch="512" dirTag="512_0_512" vehicle="4047" block="512_11_180" tripTag="30522439" />',
        '</direction>',
        '</predictions>',
        '</body>',
    )
    return ''.join(xml_response)


@all_requests
def nextbus_multistops_predictions_mock(url, request):
    xml_response = (
        '<?xml version="1.0" encoding="utf-8" ?>',
        '<body copyright="All data copyright Toronto Transit Commission 2016.">',
        '<predictions agencyTitle="Toronto Transit Commission" routeTitle="512-St Clair" routeTag="512" stopTitle="Gunns Loop At St Clair Ave West" stopTag="14688">',
        '<direction title="West - 512 St Clair towards Keele">',
        '<prediction epochTime="1456785375141" seconds="502" minutes="8" isDeparture="false" branch="512" dirTag="512_1_512" vehicle="4152" block="512_7_100" tripTag="30522772" />',
        '<prediction epochTime="1456785456074" seconds="583" minutes="9" isDeparture="false" branch="512" dirTag="512_1_512" vehicle="4181" block="512_8_120" tripTag="30522773" />',
        '<prediction epochTime="1456785620776" seconds="748" minutes="12" isDeparture="false" branch="512" dirTag="512_1_512" vehicle="4189" block="512_9_130" tripTag="30522774" />',
        '<prediction epochTime="1456785730336" seconds="857" minutes="14" isDeparture="false" branch="512" dirTag="512_1_512" vehicle="4150" block="512_20_142" tripTag="30522775" />',
        '<prediction epochTime="1456785966545" seconds="1093" minutes="18" isDeparture="false" branch="512" dirTag="512_1_512" vehicle="4143" block="512_21_152" tripTag="30522776" />',
        '</direction>',
        '</predictions>',
        '<predictions agencyTitle="Toronto Transit Commission" routeTitle="512-St Clair" routeTag="512" stopTitle="St Clair Station" stopTag="14295">',
        '<direction title="East - 512 St Clair towards St Clair Station">',
        '<prediction epochTime="1456784876112" seconds="3" minutes="0" isDeparture="false" branch="512" dirTag="512_0_512" vehicle="4065" block="512_13_210" tripTag="30522442" />',
        '<prediction epochTime="1456784906830" seconds="34" minutes="0" isDeparture="false" branch="512" dirTag="512_0_512" vehicle="4182" block="512_14_220" tripTag="30522443" />',
        '<prediction epochTime="1456785144816" seconds="272" minutes="4" isDeparture="false" branch="512" dirTag="512_0_512" vehicle="4064" block="512_15_230" tripTag="30522444" />',
        '<prediction epochTime="1456785349438" seconds="476" minutes="7" isDeparture="false" branch="512" dirTag="512_0_512" vehicle="4167" block="512_24_252" tripTag="30522445" />',
        '<prediction epochTime="1456785468328" seconds="595" minutes="9" isDeparture="false" branch="512" dirTag="512_0_512" vehicle="4197" block="512_1_10" tripTag="30522446" />',
        '</direction>',
        '</predictions>',
        '</body>'
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

    def test_get_route_config(self):
        with HTTMock(nextbus_route_config_mock):
            nb = NextBus()
            route_config = nb.get_route_config('ttc', '512')
            self.assertEqual(len(route_config['directions']), 2)
            self.assertEqual(len(route_config['stops']), 6)

    def test_get_predictions(self):
        with HTTMock(nextbus_predictions_mock):
            nb = NextBus()
            predictions = nb.get_predictions('ttc', '512', '14295')
            self.assertEqual(int(predictions[0]['seconds']), 8)  # Fake dataset, fixed value

    def test_get_first_prediction_multi_stops(self):
        with HTTMock(nextbus_multistops_predictions_mock):
            nb = NextBus()
            predictions = nb.get_first_prediction_multi_stops(
                'ttc',
                ['512|14295', '512|14688']
            )
            self.assertEqual(int(predictions[0][1]), 502)  # first prediction for first stop in fake dataset

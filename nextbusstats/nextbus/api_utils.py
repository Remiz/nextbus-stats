import requests
import xml.etree.ElementTree as ET


class NextBus():
    """Set of functions to retrieve info from NextBus api"""
    api_feed_url = 'http://webservices.nextbus.com/service/publicXMLFeed?'

    def get_agency_list(self):
        response = requests.get(self.api_feed_url+'command=agencyList')
        if response.status_code == 200:
            response_xml = response.text
        else:
            response.raise_for_status()
        root = ET.fromstring(response_xml)
        agencies = []
        for agency in root.iter('agency'):
            agencies.append(agency)
        return agencies

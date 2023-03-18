"""
Holds the main STCP widget scraper. 
Reused from a previous project - refactor pending.
"""

import urllib
from typing import Optional
from uuid import UUID, uuid4

import requests
from bs4 import BeautifulSoup

from app.models import BusStop, BusRoute


REQUEST_TIMEOUT = 10
ITINERARIUM_URL = "http://www.stcp.pt/pt/itinerarium/callservice.php?"
WIDGET_URL = "www.stcp.pt/pt/widget/post.php?"


def call_itinerarium(**kwargs: dict[str]) -> requests.Response:
    """
    Wrapper function to call the STCP Itinerarium endpoint with the provided arguments.

    Known accepted arguments:
        action=lineslist -> lists the lines
        action=linestops -> lists the stops for a given stop code lcode=<stop_code> and a direction ldir=<0|1>
    """
    url = f"{ITINERARIUM_URL}{urllib.parse.urlencode(kwargs)}"
    return requests.get(url, timeout=REQUEST_TIMEOUT)

def get_lines() -> set[BusRoute]:
    """
    Simple endpoint to get the set of available BusRoutes.
    Wrapper for one of the itinerarium endpoints.
    """
    line_data = call_itinerarium({"action": "lineslist"}).json()
    lines = {
        BusRoute(
            code=record.get('code'),
            pubcode=record.get('pubcode'),
            description=record.get('description'),
            # Empirically determining if line is circular would require a second api call per line,
            # either to check if there are no stops in line when direction is 1, or to check
            # if the first and last stops are the same when line direction is 0.
            # Hence, the following hacky, but faster approach:
            circular=('CIRCULAR' in record.get('description'))
            ) for record in line_data.get('records')}
    return lines


def get_line_stops(line: str, direction:bool = False) -> list[BusStop]:
    """
    Simple endpoint to provide the list of stops for a given route.
    Wrapper for one of the itinerarium endpoints.
    """
    ldir_str: str = "1" if direction else "0"
    request_url = f"http://www.stcp.pt/pt/itinerarium/callservice.php?action=linestops&lcode={line}&ldir={ldir_str}"
    stops_data = requests.get(request_url, timeout=10).json()
    stops = [
        BusStop(
            code=record.get('code'),
            name=record.get('name'),
            address=record.get('address'),
            zone=record.get('zone'),
        ) for record in stops_data.get('records')
    ]
    return stops


class STCPClient():
    """Client to get bus info from STCP by scraping SMSBUS"""
    def __init__(self, uid: Optional[UUID] = None):
        self.uid = uid.hex if uid else uuid4().hex
        self.link = WIDGET_URL

    def get_times(self, bus_stop: BusStop):
        """
        Get real-time next arrivals for a given stop
        """
        paragem = bus_stop.code
        request = f"http://{self.link}uid={self.uid}&paragem={paragem}"

        response = requests.get(request, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        hits = []
        for hit in soup.find_all(class_="separa"):

            # TODO: more stringent try/catch
            try:
                stop_code = hit.contents[1].contents[1].contents[1].string
                direction = hit.contents[3].contents[0].contents[0]
                time = hit.contents[5].contents[0]
                if 'a passar' not in time:
                    time = time.split(' - ')
                else:
                    time = ['now', '0min']
                hits.append([stop_code, direction, time[0], time[1]])
            except IndexError:
                pass

        # TODO: make use of warnings (elements are inside a DIV with ID = "cycle-alertas")
        warnings = soup.find(id="cycle-alertas").contents

        return hits

"""
Holds the main STCP widget scraper. 
Reused from a previous project - refactor pending.
"""

from typing import Optional
from uuid import UUID, uuid4

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class BusRoute(BaseModel, frozen=True):
    """Represents an STCP bus route"""
    code: str
    pubcode: str
    description: str
# TODO: consider circular lines


class BusStop(BaseModel, frozen=True):
    """Represents an STCP bus stop"""
    code: str
    name: str
    address: str
    zone: str


def get_lines() -> set[BusRoute]:
        """Retrieve line info from SMSBUS"""
        request_url = "http://www.stcp.pt/pt/itinerarium/callservice.php?action=lineslist"
        line_data = requests.get(request_url, timeout=9).json()
        lines = {
            BusRoute(
                code=record.get('code'),
                pubcode=record.get('pubcode'),
                description=record.get('description')
                ) for record in line_data.get('records')}
        return lines


def get_stops(line: str, direction: bool) -> list[BusStop]:
    """Get stops"""
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
    def __init__(self, uid: Optional[UUID] = None, link: str = "www.stcp.pt/pt/widget/post.php?"):
        self.uid = uid.hex if uid else uuid4().hex
        self.link = link

    def get_times(self, bus_stop: BusStop):
        """
        Get real-time next arrivals for a given stop
        """
        paragem = bus_stop.code
        request = f"http://{self.link}uid={self.uid}&paragem={paragem}"
        # &submete=Mostrar" -> doesn't seem to do anything
        # &np={'str'} -> adds to the name field in the widget display

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
        for warning in warnings:
            print(warning.string)

        return hits


def demo_function():
    """
    For debugging and proof-of-concept purposes
    """
    client = STCPClient()
    lines = client.get_lines()
    print(lines)
    line: str = '704'
    line_704_stops = client.get_stops(line, False)
    print(line_704_stops)
    line_704_1_timetable = client.get_times(line_704_stops[0])
    print(line_704_1_timetable)

if __name__ == '__main__':
    demo_function()

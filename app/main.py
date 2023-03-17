"""Starlite Test App"""

import requests
import uvicorn
from starlite import Starlite, get

from app.scraper import STCPClient, get_stops, BusRoute, BusStop


REQUEST_TIMEOUT = 10


@get("/")
def root_handler() -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return {"hello": "world"}


@get("/{line:str}/{stop:int}")
def get_timetable(line: str, stop: int) -> list[list[str]]:
    """Demo endpoint"""
    client = STCPClient()
    line_704_stops = get_stops(line, False)
    line_704_1_timetable = client.get_times(line_704_stops[stop])
    return line_704_1_timetable


@get("/lines")
def get_lines() -> set[BusRoute]:
    """
    Simple endpoint to get the set of available BusRoutes.
    Wrapper for one of the itinerarium endpoints.
    """
    request_url = "http://www.stcp.pt/pt/itinerarium/callservice.php?action=lineslist"
    line_data = requests.get(request_url, timeout=REQUEST_TIMEOUT).json()
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


app = Starlite(route_handlers=[root_handler, get_timetable, get_lines])

if __name__ == '__main__':
    uvicorn.run(app)

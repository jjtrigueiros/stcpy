"""Wrapper for STCP's Itinerarium API"""

import urllib
import requests

from stcpy.models import BusRoute, BusStop
from stcpy.lib import settings


def call_itinerarium(**kwargs: dict[str]) -> requests.Response:
    """
    Wrapper function to call the STCP Itinerarium endpoint with the provided arguments.

    Known accepted actions:
        action=lineslist
            -> lists the lines
        action=linedirslist
            -> lists the directions for a given bus line given a line code lcode=<line_code>
        action=linestops
            -> lists the stops for a given stop code lcode=<stop_code> and a direction ldir=<0|1>
        action=srchstoplines
            -> retrieves useful detailed information (such as GPS coordinates) for a given stop stopcode=<stop_code>
    """
    url = f"{settings.app.ITINERARIUM_URL}{urllib.parse.urlencode(kwargs)}"
    return requests.get(url, timeout=settings.app.REQUEST_TIMEOUT)


def get_lines() -> set[BusRoute]:
    """
    Simple endpoint to get the set of available BusRoutes.
    Wrapper for one of the itinerarium endpoints.
    """
    line_data = call_itinerarium(action="lineslist").json()
    lines = {
        BusRoute(
            code=record.get("code"),
            pubcode=record.get("pubcode"),
            description=record.get("description"),
            # Empirically determining if line is circular would require a second api call per line,
            # for the linedirslist action. While there is no cache, this approach is hacky but faster:
            circular=("CIRCULAR" in record.get("description")),
        )
        for record in line_data.get("records")
    }
    return lines


def get_line_stops(line: str, direction: bool = False) -> list[BusStop]:
    """
    Simple endpoint to provide the list of stops for a given route.
    Wrapper for one of the itinerarium endpoints.
    """
    ldir_str: str = "1" if direction else "0"
    stops_data = call_itinerarium(action="linestops", lcode=line, ldir=ldir_str).json()
    stops = [
        BusStop(
            code=record.get("code"),
            name=record.get("name"),
            address=record.get("address"),
            zone=record.get("zone"),
        )
        for record in stops_data.get("records")
    ]
    return stops

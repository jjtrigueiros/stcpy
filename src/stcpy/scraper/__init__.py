"""
Holds the main STCP widget scraper. 
Reused from a previous project - refactor pending.
"""

from typing import Optional
from uuid import UUID, uuid4

import requests
from bs4 import BeautifulSoup

from stcpy.settings import WIDGET_URL, REQUEST_TIMEOUT

from .itinerarium import get_line_stops, get_lines


__all__ = ["get_lines", "get_line_stops"]


def get_times(bus_stop_id: str, uid: Optional[UUID] = None):
    """
    Get real-time next arrivals for a given stop by scraping SMSBUS
    """
    uid = uid.hex if uid else uuid4().hex
    bus_stop_id = bus_stop_id.upper()  # case-insensitive
    request = f"{WIDGET_URL}uid={uid}&paragem={bus_stop_id}"
    response = requests.get(request, timeout=REQUEST_TIMEOUT)
    soup = BeautifulSoup(response.text, "html.parser")
    hits = []
    for hit in soup.find_all(class_="separa"):
        # TODO: more stringent try/catch
        try:
            bus_stop_id = hit.contents[1].contents[1].contents[1].string
            direction = hit.contents[3].contents[0].contents[0]
            time = hit.contents[5].contents[0]
            if "a passar" not in time:
                time = time.split(" - ")
            else:
                time = ["now", "0min"]
            hits.append([bus_stop_id, direction, time[0], time[1]])
        except IndexError:
            pass
    # TODO: make use of warnings (elements are inside a DIV with ID = "cycle-alertas")
    warnings = soup.find(id="cycle-alertas").contents
    return hits

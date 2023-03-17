"""Starlite Test App"""

import uvicorn
from starlite import Starlite, get

from app.scraper import STCPClient, get_lines, get_stops, BusRoute, BusStop


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


app = Starlite(route_handlers=[root_handler, get_timetable])

if __name__ == '__main__':
    uvicorn.run(app)

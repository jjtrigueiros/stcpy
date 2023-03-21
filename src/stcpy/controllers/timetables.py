"""Endpoint to retrieve the timetables"""

from starlite import Router, get

from stcpy.scraper import get_line_stops, get_times


@get("/")
def endpoint_help() -> list[str]:
    """Provides a hint on how to use the endpoint."""
    return ["Usage: /timetables/line_code/direction/stop_number/"]


@get("/bus/{line:str}/{direction:int}/{stop:int}")
def get_by_line_dir_stop(line: str, direction: int, stop: int) -> list[list[str]]:
    """Provided a line ID, direction and stop number, retrieves the timetable."""
    line_stops = get_line_stops(line, direction)
    line_timetable = get_times(line_stops[stop].code)
    return line_timetable


@get("/stop/{stop:str}/")
def get_by_stop_id(stop: str) -> list[list[str]]:
    """Provided a stop ID, retrieves the timetable."""
    line_timetable = get_times(stop)
    return line_timetable


router = Router(
    path="/timetables",
    route_handlers=[endpoint_help, get_by_line_dir_stop, get_by_stop_id],
)

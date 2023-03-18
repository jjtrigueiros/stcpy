from starlite import Router, get

from app.scraper import get_line_stops, STCPClient


@get("/")
def help() -> list[str]:
    return ["Usage: /timetable/line_code/direction/stop_number/"]


@get("/{line:str}/{dir:int}/{stop:int}")
def get_by_line_dir_stop(line: str, dir: int, stop: int) -> list[list[str]]:
    """Demo endpoint"""
    line_stops = get_line_stops(line, dir)
    line_timetable = STCPClient().get_times(line_stops[stop])
    return line_timetable


router = Router(
    path="/timetables",
    route_handlers=[help, get_by_line_dir_stop]
)
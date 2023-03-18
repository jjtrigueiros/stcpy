from starlite import Router

from . import timetables


__all__ = ["router"]


router = Router(
    path="/v1",
    route_handlers=[
        timetables.router
])
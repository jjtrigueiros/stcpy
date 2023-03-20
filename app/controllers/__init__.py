from starlite import Router

from . import timetables


__all__ = ["router"]


router = Router(
    path="/v0",
    route_handlers=[
        timetables.router
])

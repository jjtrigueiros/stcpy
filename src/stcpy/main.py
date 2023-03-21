"""Starlite Test App"""

from starlite import Starlite, get

from .controllers import router
from .lib import openapi


@get("/")
def root_handler() -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return {"hello": "world"}


app = Starlite(
    route_handlers=[root_handler, router],
    openapi_config=openapi.config
)

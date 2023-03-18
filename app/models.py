from pydantic import BaseModel


class BusRoute(BaseModel, frozen=True):
    """Represents an STCP bus route"""
    code: str
    pubcode: str
    description: str
    circular: bool


class BusStop(BaseModel, frozen=True):
    """Represents an STCP bus stop"""
    code: str
    name: str
    address: str
    zone: str
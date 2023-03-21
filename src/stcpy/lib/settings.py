from typing import Optional
from pydantic import BaseSettings


class AppSettings(BaseSettings):
    class Config:
        case_sensitive = True

    DEBUG: bool
    ENVIRONMENT: str
    LOG_LEVEL: str
    NAME: str
    REQUEST_TIMEOUT: int = 10
    WIDGET_URL: str = "http://www.stcp.pt/pt/widget/post.php?"
    ITINERARIUM_URL: str = "http://www.stcp.pt/pt/itinerarium/callservice.php?"


class OpenAPISettings(BaseSettings):
    class Config:
        env_prefix = "OPENAPI_"
        case_sensitive = True

    TITLE: Optional[str]
    VERSION: str
    CONTACT_NAME: str
    CONTACT_EMAIL: str


app = AppSettings()
openapi = OpenAPISettings()
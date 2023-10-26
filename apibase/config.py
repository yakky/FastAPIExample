from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "apibase"
    app_description: str = "Get information about Star Wars planets"
    app_summary: str = "Retrieve information about Star Wars planets"
    app_version: str = "0.1.0"
    app_debug: bool = False
    swapi_url: str = "https://swapi.dev/api"
    origins: list[str] = ["*"]


@lru_cache
def get_settings():
    return Settings()


tags_metadata = [
    {
        "name": "planets",
        "description": "Information about Star Wars planets.",
    },
    {
        "name": "people",
        "description": "Information about Star Wars people.",
    },
]

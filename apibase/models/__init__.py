import re

from pydantic import BaseModel, Field, field_validator, computed_field

from apibase.config import get_settings


def extract_id(url: str):
    match = re.search(rf"{get_settings().swapi_url}/planets/(\d+)/", url)
    if match:
        return match.group(1)
    return None


class Person(BaseModel):
    name: str
    birth_year: str


class Planet(BaseModel):
    name: str
    population: str
    url: int = Field(..., serialization_alias="id")

    @field_validator("url", mode="before")
    @classmethod
    def get_id(cls, v: str) -> int | None:
        """Extract the id from the planet url."""
        try:
            return int(extract_id(v))
        except ValueError:
            return None

    @computed_field
    @property
    def href(self) -> str:
        """Get the local url for the planet."""
        from apibase.main import app

        return app.url_path_for("planet", planet_id=self.url)


class PlanetDetail(Planet):
    people: list[Person]

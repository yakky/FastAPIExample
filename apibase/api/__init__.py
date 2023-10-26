from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Path

from apibase.config import get_settings, Settings
from apibase.data import get_planet_page, get_planet_data
from apibase.models import Planet, PlanetDetail

router = APIRouter()


@router.get(
    "/",
    name="index",
    tags=["planets"],
    summary="Fetch the list of planets",
    description="Fetch the list of planets from the Star Wars API",
)
async def planets(settings: Annotated[Settings, Depends(get_settings)]) -> list[Planet]:
    async with httpx.AsyncClient() as client:
        planets = []
        async for planet in get_planet_page(
            client, settings, "https://swapi.dev/api/planets/"
        ):
            planets.append(planet)
        return planets


@router.get(
    "/planet/{planet_id}/",
    name="planet",
    tags=["planets", "people"],
    summary="Get the details of a planet",
    description="Planet details from the Star Wars API",
)
async def planet_detail(
    settings: Annotated[Settings, Depends(get_settings)],
    planet_id: Annotated[int, Path(description="ID of the planet to fetch")],
) -> PlanetDetail:
    async with httpx.AsyncClient() as client:
        data = await get_planet_data(client, settings, planet_id)
    return data

import asyncio
from typing import AsyncIterable

import httpx

from apibase.config import Settings


async def get_planet_page(
    client: httpx.AsyncClient, settings: Settings, url: str
) -> AsyncIterable[dict[str, str]]:
    """
    Async generator to get the planets from swapi.

    Pages are retrieved recursively if next_url is set.
    """
    response = await client.get(url)
    data = response.json()
    next_url = data["next"]
    try:
        for planet in data["results"]:
            yield planet
    except KeyError:
        pass
    if next_url:
        async for planet in get_planet_page(client, settings, next_url):
            yield planet


async def get_planet_data(
    client: httpx.AsyncClient, settings: Settings, planet_id: int
) -> dict[str, str | tuple[dict[str, str]] | list[str]]:
    """Get planet details."""
    response = await client.get(f"{settings.swapi_url}/planets/{planet_id}/")
    data = response.json()
    residents = await asyncio.gather(
        *[get_person(client, person) for person in data["residents"]]
    )
    data["people"] = residents
    return data


async def get_person(client: httpx.AsyncClient, url: str) -> dict[str, str]:
    """Get person details."""
    response = await client.get(url)
    data = response.json()
    return data

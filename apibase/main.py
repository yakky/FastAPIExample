from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from .api import router as internal_router
from .config import get_settings, tags_metadata

app = FastAPI(
    title=get_settings().app_name,
    description=get_settings().app_description,
    summary=get_settings().app_summary,
    version=get_settings().app_version,
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(internal_router)


@app.get("/items/{item_id}", response_model=dict[str, str])
async def get_item(item_id: int, q: Annotated[str | None, Query()] = None):
    return {
        "name": f"ciao {item_id}",
        "q": f"ciao {q or ''}",
    }

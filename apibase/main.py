from fastapi import FastAPI
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

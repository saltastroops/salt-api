from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from app.dependencies import get_db, get_settings
from app.routers.auth import router as auth_router
from app.routers.proposals import router as proposals_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(proposals_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event() -> None:
    """Connect to the SALT Science Database."""
    settings = get_settings()
    if settings.sdb_dsn:  # the DSN is not defined for unit tests
        await get_db.connect(settings.sdb_dsn)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Close the database connection."""
    await get_db.close()


def _is_api_request(request: Request) -> bool:
    """Check whether a request is an API request."""

    return request.url.path.startswith("/api/") or request.url.path.startswith("api/")


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Error handler for HTTP exceptions.

    For API requests a JSON object with a detail property is returned.

    For web page requests a redirection response (for Authorization exceptions, i.e.
    for exceptions with a status code of 401)
    """
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

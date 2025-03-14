from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from saltapi.exceptions_handling import setup_exception_handler
from saltapi.logging_config import setup_logging
from saltapi.settings import get_settings
from saltapi.web.api.authentication import router as authentication_router
from saltapi.web.api.block_visits import router as block_visits_router
from saltapi.web.api.blocks import router as blocks_router
from saltapi.web.api.finder_charts import router as finder_charts_router
from saltapi.web.api.institutions import router as institution_router
from saltapi.web.api.instruments import router as instruments_router
from saltapi.web.api.proposal_progress import router as progress_router
from saltapi.web.api.proposals import router as proposals_router
from saltapi.web.api.salt_astronomers import router as salt_astronomers_router
from saltapi.web.api.submissions import router as submissions_router
from saltapi.web.api.user import router as user_router
from saltapi.web.api.users import router as users_router
from saltapi.web.api.status import router as status_router

app = FastAPI()


settings = get_settings()

setup_logging(app)
setup_exception_handler(app)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=settings.allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    max_age=3600 * settings.auth_token_lifetime_hours,
)

app.include_router(progress_router)
app.include_router(blocks_router)
app.include_router(proposals_router)
app.include_router(authentication_router)
app.include_router(block_visits_router)
app.include_router(user_router)
app.include_router(users_router)
app.include_router(instruments_router)
app.include_router(institution_router)
app.include_router(salt_astronomers_router)
app.include_router(submissions_router)
app.include_router(finder_charts_router)
app.include_router(status_router)

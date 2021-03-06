"""The server for the SALT API."""
import pathlib
from typing import Any, Dict

import dotenv
from ariadne import (
    MutationType,
    ScalarType,
    SubscriptionType,
    load_schema_from_path,
    make_executable_schema,
)
from ariadne.asgi import GraphQL
from pydantic import ValidationError
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from saltapi import routes
from saltapi.auth.authorization import TokenAuthenticationBackend
from saltapi.graphql import resolvers, scalars
from saltapi.graphql.directives import PermittedForDirective
from saltapi.repository.database import database
from saltapi.util.error import UsageError
import logging
dotenv.load_dotenv()

# error handling
logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s [%(levelname)s]:[%(filename)s, line %(lineno)d]. %(message)s.",
                    datefmt='%Y/%m/%d %H:%M:%S', level=logging.INFO)


def error_response(detail: str, status_code: int) -> Response:
    """JSON response returned for an error."""
    return JSONResponse({"detail": detail}, status_code=status_code)


async def http_exception(request: Request, e: HTTPException) -> Response:
    """Handle a HTTPException."""
    return error_response(e.detail, e.status_code)


async def usage_error(request: Request, e: UsageError) -> Response:
    """Handle a user error."""
    return error_response(str(e), e.status_code)


async def validation_error(request: Request, e: ValidationError) -> Response:
    """Handle a validation error raised by pydantic."""
    return error_response(str(e), 400)


exception_handlers: Dict[Any, Any] = {
    HTTPException: http_exception,
    UsageError: usage_error,
    ValidationError: validation_error,
}


# middleware

middleware = [
    Middleware(AuthenticationMiddleware, backend=TokenAuthenticationBackend())
]


# GraphQL

schema_path = (
    pathlib.Path(__file__).parent.absolute().joinpath("graphql", "schema.graphql")
)
type_defs = load_schema_from_path("saltapi/graphql/schema.graphql")

datetime_scalar = ScalarType("Datetime")
datetime_scalar.set_serializer(scalars.serialize_datetime)
datetime_scalar.set_value_parser(scalars.parse_datetime)

proposal_code_scalar = ScalarType("ProposalCode")
proposal_code_scalar.set_serializer(scalars.serialize_proposal_code)
proposal_code_scalar.set_value_parser(scalars.parse_proposal_code)

mutation = MutationType()
mutation.set_field("submitProposal", resolvers.resolve_submit_proposal)

subscription = SubscriptionType()
subscription.set_field("submissionProgress", resolvers.resolve_submission_progress)
subscription.set_source("submissionProgress", resolvers.submission_progress_generator)

schema = make_executable_schema(
    type_defs,
    datetime_scalar,
    proposal_code_scalar,
    mutation,
    subscription,
    directives={"permittedFor": PermittedForDirective},
)


# non-GraphQL routes


async def token(request: Request) -> Response:
    """Request an authentication token."""
    return await routes.token(request)


async def public_key(request: Request) -> Response:
    """Request the public key for token authentication."""
    return await routes.public_key(request)


non_graphql_routes = [
    Route("/token", token, methods=["POST"]),
    Route("/public-key", public_key, methods=["GET"]),
]


# create the app

app = Starlette(
    middleware=middleware,
    exception_handlers=exception_handlers,
    routes=non_graphql_routes,
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)
app.mount("/graphql", GraphQL(schema))

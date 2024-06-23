import argparse
import logging
import os
import typing

import fastapi
import sentry_sdk
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware

from babyhelm.containers.application import ApplicationContainer
from babyhelm.exception_handlers import exception_handlers_list
from babyhelm.routers import routers_list


def get_container() -> ApplicationContainer:
    """Get container."""
    if "CONFIG" not in os.environ:
        raise TypeError("Key 'CONFIG' not found in env variables")
    if os.path.exists(os.environ["CONFIG"]) is False:
        raise FileNotFoundError(
            'Config not found "{0}"'.format(os.environ["CONFIG"]),
        )
    container = ApplicationContainer()
    container.config.from_yaml(os.environ["CONFIG"])
    return container


class ArgsNamespace(argparse.Namespace):
    """Args namespace."""

    config: str
    host: str
    port: int
    workers: int
    debug: bool
    reload: bool
    log_level: str
    lifespan: str


def server_parser_args() -> typing.Type[ArgsNamespace]:  # noqa: WPS213
    """Server parser args."""
    parser = argparse.ArgumentParser(description="BabyHelm server")
    parser.add_argument("--config", dest="config", type=str, required=True)
    parser.add_argument("--host", dest="host", type=str, default="127.0.0.1")
    parser.add_argument("--port", dest="port", type=int, default=8000)
    parser.add_argument("--workers", default=1, type=int)
    parser.add_argument(
        "--reload",
        default=True,
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        type=str,
        default="info",
        choices=["critical", "error", "warning", "info", "debug", "trace"],
    )
    return parser.parse_args(namespace=ArgsNamespace)


def create_app(container: ApplicationContainer | None = None):
    """Create app."""
    if container is None:
        container = get_container()

    debug: bool = container.config.get("debug")

    sentry_sdk.init(
        dsn="https://63a3a9faafa24c6a9a7eedbf61828ec1@o4506655030378496.ingest.us.sentry.io/4507436787433472",
        # noqa E501
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    app = fastapi.FastAPI(
        description="BabyHelm",
        debug=debug,
        openapi_url="/api/v1/openapi.json" if debug is True else None,
        docs_url="/docs" if debug is True else None,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    Instrumentator(excluded_handlers=["/metrics"]).instrument(app).expose(app)

    for router in routers_list:
        app.include_router(router)

    for handler_info in exception_handlers_list:
        app.add_exception_handler(**handler_info)

    app.state.container = container

    return app


def main() -> None:
    """."""
    args: typing.Type[ArgsNamespace] = server_parser_args()
    if os.environ.get("RUNNING_ENV") == "production":
        args.config = "/app/config/prod.yaml"
        logging.info("Running in production mode")

    os.environ["CONFIG"] = args.config

    uvicorn.run(
        "babyhelm.app:create_app",
        host=args.host,
        port=args.port,
        workers=args.workers,
        factory=True,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()

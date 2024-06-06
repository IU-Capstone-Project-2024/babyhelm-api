import argparse
import os
import typing

import fastapi
import uvicorn

from babyhelm.containers.application import ApplicationContainer
from babyhelm.routers.test import router


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

    app = fastapi.FastAPI(
        description="BabyHelm",
        debug=debug,
        openapi_url="/api/v1/openapi.json" if debug is True else None,
        docs_url="/docs" if debug is True else None,
    )

    app.include_router(router, tags=["tg"])

    app.state.container = container

    return app


def main() -> None:
    """."""
    args: typing.Type[ArgsNamespace] = server_parser_args()

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

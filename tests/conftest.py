import os
from unittest import mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession

from babyhelm.app import create_app
from babyhelm.containers.application import ApplicationContainer
from babyhelm.gateways.database import Database
from babyhelm.models import Base

CONFIG_FILE = "config/config.test.yaml"
MOCK_DB_URL = "sqlite+aiosqlite:///test.db"
MOCK_DB_URL_SYNC = "sqlite:///test.db"


@pytest.fixture()
def fastapi_test_client(app_container: ApplicationContainer) -> TestClient:
    os.environ["CONFIG"] = CONFIG_FILE
    app = create_app()
    app.state.container.override(app_container)
    return TestClient(app)


@pytest.fixture(name="session")
def session_mock() -> AsyncSession:
    """Session mock."""
    execute_res = mock.Mock()
    execute_res.scalar_one_or_none.return_value = True

    session = mock.Mock(spec=AsyncSession)
    session.execute = mock.AsyncMock(return_value=execute_res)
    return session


@pytest.fixture()
def app_container(database: Database) -> ApplicationContainer:
    """App container."""
    container = ApplicationContainer()
    container.config.from_yaml(CONFIG_FILE)
    container.gateways.db.override(database)
    return container


@pytest.fixture()
def _setup_tables():
    engine = create_engine(url=MOCK_DB_URL_SYNC)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
def database(_setup_tables):
    return Database(url=MOCK_DB_URL)

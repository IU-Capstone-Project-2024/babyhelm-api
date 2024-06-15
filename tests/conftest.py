import os
from unittest import mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from babyhelm.app import create_app
from babyhelm.containers.application import ApplicationContainer
from babyhelm.gateways.database import Database


@pytest.fixture()
def fastapi_test_client(container: ApplicationContainer) -> TestClient:
    os.environ["CONFIG"] = "config/config.test.yaml"
    app = create_app()
    app.state.container = container
    return TestClient(app)


@pytest.fixture(name="session")
def session_mock() -> AsyncSession:
    """Session mock."""
    execute_res = mock.Mock()
    execute_res.scalar_one_or_none.return_value = True

    session = mock.Mock(spec=AsyncSession)
    session.execute = mock.AsyncMock(return_value=execute_res)
    return session


@pytest.fixture(name="db")
def db_mock(session: AsyncSession) -> Database:
    """Database mock."""
    db = mock.AsyncMock(spec=Database)
    db.session.return_value.__aenter__.return_value = session
    return db


@pytest.fixture(name="container")
def app_container(db: Database) -> ApplicationContainer:
    """App container."""
    container = ApplicationContainer()
    container.config.from_yaml("config/config.test.yaml")
    container.gateways.db.override(db)
    return container

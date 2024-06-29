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
from babyhelm.schemas.manifest_builder import Application, Project
from babyhelm.schemas.user import UserSchema

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


@pytest.fixture()
def application_values_as_dict() -> dict:
    return {
        "name": "some-app",
        "image": "some-image:latest",
        "ports": {"port": 80, "targetPort": 8000},
        "envs": [{"name": "SOME_ENV", "value": "SOME_VALUE"}],
    }


@pytest.fixture()
def application_values(application_values_as_dict) -> Application:
    return Application.model_validate(application_values_as_dict)


@pytest.fixture()
def render_application_results() -> dict:
    return {
        "deployment": {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": "some-app-deployment"},
            "spec": {
                "strategy": {
                    "type": "RollingUpdate",
                    "rollingUpdate": {"maxSurge": 1, "maxUnavailable": 1},
                },
                "selector": {"matchLabels": {"app": "some-app"}},
                "replicas": 2,
                "template": {
                    "metadata": {"labels": {"app": "some-app"}},
                    "spec": {
                        "containers": [
                            {
                                "name": "some-app-container",
                                "image": "some-image:latest",
                                "ports": [{"containerPort": 8000}],
                                "env": [{"name": "SOME_ENV", "value": "SOME_VALUE"}],
                            }
                        ]
                    },
                },
            },
        },
        "service": {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": "some-app-svc", "labels": {"app": "some-app"}},
            "spec": {
                "type": "LoadBalancer",
                "loadBalancerClass": "tailscale",
                "ports": [{"port": 80, "targetPort": 8000}],
                "selector": {"app": "some-app"},
            },
        },
        "hpa": {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {"name": "some-app-autoscaler"},
            "spec": {
                "maxReplicas": 5,
                "metrics": [
                    {
                        "resource": {
                            "name": "cpu",
                            "target": {"averageUtilization": 30, "type": "Utilization"},
                        },
                        "type": "Resource",
                    },
                    {
                        "resource": {
                            "name": "memory",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": 250,
                            },
                        },
                        "type": "Resource",
                    },
                ],
                "minReplicas": 2,
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": "some-app-deployment",
                },
            },
        },
    }


@pytest.fixture()
def namespace_values_as_dict() -> dict:
    return {"name": "MyPerfectApp"}


@pytest.fixture()
def namespace_values(namespace_values_as_dict) -> Project:
    return Project.model_validate(namespace_values_as_dict)


@pytest.fixture()
def render_namespace_results():
    return {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {"name": "MyPerfectApp"},
    }


@pytest.fixture()
def sample_user():
    return UserSchema(
            id=1,
            email="string@gmail.com"
    )

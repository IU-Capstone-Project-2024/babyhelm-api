import os

import pytest
from fastapi.testclient import TestClient

from babyhelm.app import create_app


@pytest.fixture()
def fastapi_test_client() -> TestClient:
    os.environ["CONFIG"] = "config/config.test.yaml"
    app = create_app()
    return TestClient(app)

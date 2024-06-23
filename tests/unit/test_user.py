from unittest import mock

import pytest
from sqlalchemy.exc import IntegrityError
from starlette.testclient import TestClient

from babyhelm.containers.application import ApplicationContainer
from babyhelm.repositories.user import UserRepository
from babyhelm.services.user import UserService


@pytest.fixture()
def user_repository_fixture():
    return mock.AsyncMock(spec=UserRepository)


@pytest.mark.asyncio()
class TestUser:
    async def test_repository_create(self, app_container: ApplicationContainer):
        user_repository_mock = mock.AsyncMock(spec=UserRepository)

        app_container.repositories.user.override(user_repository_mock)

        user_service: UserService = app_container.services.user()

        user_repository_mock.create.side_effect = IntegrityError(
            "statement", {}, Exception()
        )
        with pytest.raises(IntegrityError):
            await user_service.create("example.com", raw_password="password")

    async def test_user_register_endpoint_422(
        self,
        fastapi_test_client: TestClient,
    ):
        response = fastapi_test_client.post(
            "/users/registration",
            json={
                "email": "email",
                "raw_password": "password",
            },
        )
        assert response.status_code == 422

    async def test_user_register_endpoint_201(self, fastapi_test_client: TestClient):
        response = fastapi_test_client.post(
            "/users/registration",
            json={
                "email": "email@example.com",
                "raw_password": "string",
            },
        )
        assert response.status_code == 201

    async def test_user_register_endpoint_201_400(
        self, fastapi_test_client: TestClient
    ):
        response1 = fastapi_test_client.post(
            "/users/registration",
            json={
                "email": "email@example.com",
                "raw_password": "string",
            },
        )
        response2 = fastapi_test_client.post(
            "/users/registration",
            json={
                "email": "email@example.com",
                "raw_password": "string",
            },
        )

        assert response1.status_code == 201
        assert response2.status_code == 400

    async def test_user_login_endpoint(self, fastapi_test_client: TestClient):
        register_response = fastapi_test_client.post(
            "/users/registration",
            json={
                "email": "email@example.com",
                "raw_password": "string",
            },
        )

        assert register_response.status_code == 201

        login_response_200 = fastapi_test_client.post(
            "/users/login",
            json={
                "email": "email@example.com",
                "raw_password": "string",
            },
        )

        login_response_400 = fastapi_test_client.post(
            "/users/login",
            json={
                "email": "email1@example.com",
                "raw_password": "string",
            },
        )

        assert login_response_200.status_code == 200
        assert login_response_400.status_code == 400

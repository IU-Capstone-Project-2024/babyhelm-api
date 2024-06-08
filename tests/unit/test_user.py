from unittest import mock

import pytest
from sqlalchemy.exc import IntegrityError
from starlette.testclient import TestClient

from babyhelm.containers.application import ApplicationContainer
from babyhelm.repositories.user import UserRepository
from babyhelm.services.user import UserService


@pytest.fixture(name="user_repo")
def user_repository_fixture():
    return mock.AsyncMock(spec=UserRepository)


@pytest.fixture(name="user_service")
def user_service(user_repo) -> UserService:
    return UserService(user_repo)


@pytest.mark.asyncio()
class TestUser:
    async def test_repository_create(self,
                                     container: ApplicationContainer):
        user_repository_mock = mock.AsyncMock(spec=UserRepository)

        container.repositories.user.override(user_repository_mock)

        user_service: UserService = container.services.user()

        user_repository_mock.create.side_effect = IntegrityError("statement", {}, Exception())
        with pytest.raises(IntegrityError):
            await user_service.create("example.com", raw_password="password")

    async def test_user_register_endpoint_422(self,
                                              fastapi_test_client: TestClient,
                                              ):
        user_repository = mock.AsyncMock(spec=UserRepository)
        user_repository.create.return_value = None
        fastapi_test_client.app.state.container.repositories.user.override(user_repository)

        response = fastapi_test_client.post(
            "/users/registration",
            json={
                "email": "email",
                "raw_password": "password",

            }
        )
        assert response.status_code == 422

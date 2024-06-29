from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from kubernetes.utils import FailToCreateError
from sqlalchemy.exc import SQLAlchemyError

from babyhelm.exceptions.cluster_manager import ClusterError, DatabaseError
from babyhelm.repositories.application import ApplicationRepository
from babyhelm.repositories.project import ProjectRepository
from babyhelm.schemas.cluster_manager import (
    CreateApplicationRequest,
    CreateApplicationResponse,
    CreateProjectResponse,
)
from babyhelm.schemas.manifest_builder import (
    Application,
    ApplicationManifests,
    Env,
    NamespaceManifest,
    Ports,
    Project,
)
from babyhelm.services.cluster_manager import ClusterManagerService
from babyhelm.services.manifest_builder import ManifestBuilderService


class MockAPIException:
    reason = "MockAPIExceptionReason"
    body = "MockAPIExceptionBody"


@pytest.fixture()
def project_repository():
    return AsyncMock(spec=ProjectRepository)


@pytest.fixture()
def application_repository():
    return AsyncMock(spec=ApplicationRepository)


@pytest.fixture()
def manifest_builder(render_application_results, render_namespace_results):
    builder = MagicMock(spec=ManifestBuilderService)
    builder.render_namespace.return_value = NamespaceManifest(
        namespace=render_namespace_results
    )
    builder.render_application.return_value = ApplicationManifests(
        **render_application_results
    )
    return builder


@pytest.fixture()
def kubeconfig_path(tmp_path):
    # Create a dummy kubeconfig file
    kubeconfig = tmp_path / "kubeconfig"
    kubeconfig.write_text("dummy_kubeconfig_content")
    return str(kubeconfig)


@pytest.fixture()
def host_postfix():
    return "example.com"


@pytest.fixture()
def cluster_manager_service(
    project_repository,
    application_repository,
    manifest_builder,
    kubeconfig_path,
    host_postfix,
):
    with patch("kubernetes.config.new_client_from_config_dict") as mock_k8s_client:
        mock_k8s_client.return_value = MagicMock()
        return ClusterManagerService(
            project_repository=project_repository,
            application_repository=application_repository,
            manifest_builder=manifest_builder,
            kubeconfig_path=kubeconfig_path,
            host_postfix=host_postfix,
        )


# Sample objects for testing
@pytest.fixture()
def sample_project():
    return Project(name="sampleProject")


@pytest.fixture()
def sample_application():
    ports = Ports(port=80, targetPort=80)
    envs = [Env(name="config_path", value="Users/admin/config/path")]
    return Application(name="sample_app", image="sample_image", ports=ports, envs=envs)


@pytest.fixture()
def create_application_request(sample_project, sample_application):
    return CreateApplicationRequest(
        project=sample_project, application=sample_application
    )


class TestClusterManagerService:
    def test_create_app_link(self, cluster_manager_service):
        result = cluster_manager_service._create_app_link("test_project", "test_app")
        assert result == "test_project-test_app-example.com"

    @pytest.mark.asyncio()
    async def test_create_project_success(
        self,
        cluster_manager_service,
        sample_project,
        project_repository,
        manifest_builder,
    ):
        response = await cluster_manager_service.create_project(sample_project)
        assert isinstance(response, CreateProjectResponse)
        project_repository.create.assert_called_once_with(name=sample_project.name)
        manifest_builder.render_namespace.assert_called_once_with(
            project=sample_project
        )

    @pytest.mark.asyncio()
    async def test_create_project_database_error(
        self, cluster_manager_service, sample_project, project_repository
    ):
        project_repository.create.side_effect = SQLAlchemyError
        with pytest.raises(DatabaseError):
            await cluster_manager_service.create_project(sample_project)
        project_repository.create.assert_called_once_with(name=sample_project.name)

    @pytest.mark.asyncio()
    async def test_create_project_cluster_error(
        self,
        cluster_manager_service,
        sample_project,
        project_repository,
        manifest_builder,
    ):
        with patch("kubernetes.utils.create_from_dict") as mock_create_from_dict:
            mock_create_from_dict.side_effect = FailToCreateError([MockAPIException()])
            with pytest.raises(ClusterError):
                await cluster_manager_service.create_project(sample_project)
            project_repository.create.assert_called_once_with(name=sample_project.name)
            project_repository.delete.assert_called_once_with(name=sample_project.name)
            manifest_builder.render_namespace.assert_called_once_with(
                project=sample_project
            )

    @pytest.mark.asyncio()
    async def test_create_application_success(
        self,
        cluster_manager_service,
        create_application_request,
        application_repository,
        manifest_builder,
    ):
        response = await cluster_manager_service.create_application(
            create_application_request
        )
        assert isinstance(response, CreateApplicationResponse)
        assert response.app_link == "sampleProject-sample_app-example.com"
        application_repository.create.assert_called_once()
        manifest_builder.render_application.assert_called_once_with(
            application=create_application_request.application
        )

    @pytest.mark.asyncio()
    async def test_create_application_database_error(
        self,
        cluster_manager_service,
        create_application_request,
        application_repository,
    ):
        application_repository.create.side_effect = SQLAlchemyError
        with pytest.raises(DatabaseError):
            await cluster_manager_service.create_application(create_application_request)
        application_repository.create.assert_called_once()

    @pytest.mark.asyncio()
    async def test_create_application_cluster_error(
        self,
        cluster_manager_service,
        create_application_request,
        application_repository,
        manifest_builder,
    ):
        with patch("kubernetes.utils.create_from_dict") as mock_create_from_dict:
            mock_create_from_dict.side_effect = FailToCreateError([MockAPIException()])
            with pytest.raises(ClusterError):
                await cluster_manager_service.create_application(
                    create_application_request
                )
            application_repository.create.assert_called_once()
            application_repository.delete.assert_called_once_with(
                name=create_application_request.application.name,
                project_name=create_application_request.project.name,
            )
            manifest_builder.render_application.assert_called_once_with(
                application=create_application_request.application
            )
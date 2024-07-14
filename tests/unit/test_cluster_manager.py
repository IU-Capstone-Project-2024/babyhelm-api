from unittest.mock import MagicMock, patch

import pytest
from kubernetes import client
from kubernetes.utils import FailToCreateError
from sqlalchemy.exc import SQLAlchemyError

from babyhelm.exceptions.cluster_manager import ClusterError, DatabaseError
from babyhelm.schemas.cluster_manager import (
    ApplicationWithLinkSchema,
    CreateApplicationRequest,
    ProjectSchema,
)
from babyhelm.schemas.manifest_builder import ApplicationManifests, NamespaceManifest
from babyhelm.services.cluster_manager import ClusterManagerService
from babyhelm.services.manifest_builder import ManifestBuilderService


class MockAPIException:
    reason = "MockAPIExceptionReason"
    body = "MockAPIExceptionBody"


@pytest.fixture()
def manifest_builder_service(render_application_results, render_project_results):
    builder = MagicMock(spec=ManifestBuilderService)
    builder.render_namespace.return_value = NamespaceManifest(
        namespace=render_project_results
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
    manifest_builder_service,
    kubeconfig_path,
    host_postfix,
    user_repository,
):
    with patch("kubernetes.config.new_client_from_config_dict") as mock_k8s_client:
        mock_k8s_client.return_value = MagicMock()
        return ClusterManagerService(
            project_repository=project_repository,
            application_repository=application_repository,
            manifest_builder=manifest_builder_service,
            user_repository=user_repository,
            kubeconfig_path=kubeconfig_path,
            host_postfix=host_postfix,
        )


@pytest.fixture()
def create_application_request(application_values):
    return CreateApplicationRequest(application=application_values)


class TestClusterManagerService:
    def test_create_app_link(self, cluster_manager_service):
        result = cluster_manager_service._create_app_link("test_project", "test_app")
        assert result == "test_project-test_app-example.com"

    @pytest.mark.asyncio()
    async def test_create_project_success(
        self,
        cluster_manager_service,
        project_repository,
        manifest_builder_service,
        project_values,
        sample_user,
        sample_user_model,
    ):
        response = await cluster_manager_service.create_project(
            project_values, sample_user.id
        )
        assert isinstance(response, ProjectSchema)
        project_repository.create.assert_called_once_with(
            name=project_values.name, user=sample_user_model
        )
        manifest_builder_service.render_namespace.assert_called_once_with(
            project=project_values
        )

    @pytest.mark.asyncio()
    async def test_create_project_database_error(
        self,
        cluster_manager_service,
        project_repository,
        project_values,
        sample_user,
        sample_user_model,
    ):
        project_repository.create.side_effect = SQLAlchemyError
        with pytest.raises(DatabaseError):
            await cluster_manager_service.create_project(project_values, sample_user.id)
        project_repository.create.assert_called_once_with(
            name=project_values.name, user=sample_user_model
        )

    @pytest.mark.asyncio()
    async def test_create_project_cluster_error(
        self,
        cluster_manager_service,
        manifest_builder_service,
        project_repository,
        project_values,
        sample_user,
        sample_project_model,
        sample_user_model,
    ):
        with patch("kubernetes.utils.create_from_dict") as mock_create_from_dict:
            mock_create_from_dict.side_effect = FailToCreateError([MockAPIException()])
            with pytest.raises(ClusterError):
                await cluster_manager_service.create_project(
                    project_values, sample_user.id
                )
            project_repository.create.assert_called_once_with(
                name=project_values.name, user=sample_user_model
            )
            project_repository.delete.assert_called_once_with(sample_project_model)
            manifest_builder_service.render_namespace.assert_called_once_with(
                project=project_values
            )

    @pytest.mark.asyncio()
    async def test_create_application_success(
        self,
        cluster_manager_service,
        manifest_builder_service,
        application_repository,
        create_application_request,
        project_values,
    ):
        response = await cluster_manager_service.create_application(
            create_application_request, project_values.name
        )
        assert isinstance(response, ApplicationWithLinkSchema)
        assert response.deployment_link == "MyPerfectApp-some-app-example.com"
        application_repository.create.assert_called_once()
        manifest_builder_service.render_application.assert_called_once_with(
            application=create_application_request.application
        )

    @pytest.mark.asyncio()
    async def test_create_application_database_error(
        self,
        cluster_manager_service,
        application_repository,
        create_application_request,
        project_values,
    ):
        application_repository.create.side_effect = SQLAlchemyError
        with pytest.raises(DatabaseError):
            await cluster_manager_service.create_application(
                create_application_request, project_values.name
            )
        application_repository.create.assert_called_once()

    @pytest.mark.asyncio()
    async def test_create_application_cluster_error(
        self,
        cluster_manager_service,
        manifest_builder_service,
        application_repository,
        create_application_request,
        sample_application_model,
        project_values,
    ):
        with patch("kubernetes.utils.create_from_dict") as mock_create_from_dict:
            mock_create_from_dict.side_effect = FailToCreateError([MockAPIException()])
            with pytest.raises(ClusterError):
                await cluster_manager_service.create_application(
                    create_application_request, project_values.name
                )
            application_repository.create.assert_called_once()
            application_repository.delete.assert_called_once_with(
                application=sample_application_model,
            )
            manifest_builder_service.render_application.assert_called_once_with(
                application=create_application_request.application
            )

    @pytest.mark.asyncio()
    async def test_get_application_logs_success(
        self, cluster_manager_service, sample_application_model
    ):
        v1_api_mock = MagicMock()
        apps_v1_api_mock = MagicMock()

        deployment = MagicMock()
        deployment.spec.selector.match_labels = {
            "app": sample_application_model.deployment_name
        }

        apps_v1_api_mock.read_namespaced_deployment.return_value = deployment
        pod1 = MagicMock()
        pod2 = MagicMock()
        pod1.metadata.name = "pod-1"
        pod2.metadata.name = "pod-2"

        v1_api_mock.list_namespaced_pod.return_value = MagicMock(items=[pod1, pod2])
        v1_api_mock.read_namespaced_pod_log.side_effect = [
            "log-1-of-pod-1\nlog-2-of-pod-1",
            "log-1-of-pod-2\nlog-2-of-pod-2",
        ]

        with patch.object(client, "CoreV1Api", return_value=v1_api_mock):
            with patch.object(client, "AppsV1Api", return_value=apps_v1_api_mock):
                logs = await cluster_manager_service.get_application_logs(
                    sample_application_model.project_name, sample_application_model.name
                )

        assert {
            "pod-1": ["log-1-of-pod-1", "log-2-of-pod-1"],
            "pod-2": ["log-1-of-pod-2", "log-2-of-pod-2"],
        } == logs
        apps_v1_api_mock.read_namespaced_deployment.assert_called_once_with(
            name=sample_application_model.deployment_name,
            namespace=sample_application_model.project_name,
        )
        v1_api_mock.list_namespaced_pod.assert_called_once_with(
            namespace=sample_application_model.project_name,
            label_selector=f"app={sample_application_model.deployment_name}",
        )
        assert v1_api_mock.read_namespaced_pod_log.call_count == 2

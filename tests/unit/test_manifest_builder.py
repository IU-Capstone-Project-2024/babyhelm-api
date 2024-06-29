from copy import deepcopy
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from babyhelm.schemas.manifest_builder import Application, Project
from babyhelm.services.manifest_builder import ManifestBuilderService


@pytest.fixture()
def builder() -> ManifestBuilderService:
    return ManifestBuilderService(Path("babyhelm/templates"))


@pytest.fixture()
def invalid_application_values_as_dict(application_values_as_dict) -> dict:
    invalid_name = deepcopy(application_values_as_dict)
    invalid_name["name"] = "some-app{"
    invalid_image = deepcopy(application_values_as_dict)
    invalid_image["image"] = "some-image&:latest"
    invalid_env = deepcopy(application_values_as_dict)
    invalid_env["envs"][0]["name"] = "SOME@ENV"
    return {
        "invalid_name": invalid_name,
        "invalid_image": invalid_image,
        "invalid_env": invalid_env,
    }


class TestManifestBuilder:
    @pytest.mark.parametrize("manifest_type", ["deployment", "service", "hpa"])
    def test_build_manifests(
        self,
        builder: ManifestBuilderService,
        application_values: Application,
        render_application_results: dict,
        manifest_type: str,
    ):
        manifests = builder.render_application(application_values)
        assert getattr(manifests, manifest_type) == render_application_results.get(
            manifest_type
        )

    def test_manifests_endpoint(
        self,
        fastapi_test_client: TestClient,
        application_values_as_dict: dict,
        render_application_results: dict,
    ):
        response = fastapi_test_client.post(
            "/manifests/render", json=application_values_as_dict
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["deployment"] == render_application_results["deployment"]
        assert response_data["service"] == render_application_results["service"]
        assert response_data["hpa"] == render_application_results["hpa"]

    @pytest.mark.parametrize(
        "invalid_input_type", ["invalid_name", "invalid_image", "invalid_env"]
    )
    def test_manifests_endpoint_validation(
        self,
        fastapi_test_client: TestClient,
        application_values_as_dict: dict,
        render_application_results: dict,
        invalid_application_values_as_dict: dict,
        invalid_input_type: str,
    ):
        response = fastapi_test_client.post(
            "/manifests/render",
            json=invalid_application_values_as_dict[invalid_input_type],
        )
        assert response.status_code == 422

    def test_render_namespace_manifest(
        self,
        builder: ManifestBuilderService,
        namespace_values: Project,
        render_namespace_results: dict,
    ):
        namespace_manifest = builder.render_namespace(namespace_values)
        assert namespace_manifest.namespace == render_namespace_results

from pathlib import Path

import pytest
import yaml
from starlette.testclient import TestClient

from babyhelm.schemas.manifest_builder import App, Service, Values
from babyhelm.services.manifest_builder import ManifestBuilderService


@pytest.fixture()
def builder() -> ManifestBuilderService:
    return ManifestBuilderService(Path("babyhelm/templates"))


@pytest.fixture()
def app_values() -> Values:
    return Values(
            app=App(
                    name="my-app",
                    image="my-image:latest",
                    port=80,
                    service=Service(name="my-service")
            )
    )


@pytest.fixture()
def deployment_as_dict() -> dict:
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "my-app"
        },
        "spec": {
            "selector": {
                "matchLabels": {
                    "app": "my-app"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "my-app"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "my-app",
                            "image": "my-image:latest",
                            "ports": [
                                {
                                    "containerPort": 80
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }


@pytest.fixture()
def service_as_dict() -> dict:
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": "my-service"
        },
        "spec": {
            "selector": {
                "app": "my-app"
            },
            "ports": [
                {
                    "protocol": "TCP",
                    "port": 80,
                    "targetPort": 80
                }
            ]
        }
    }


class TestManifestBuilder:
    def test_build_deployment_manifest(self,
                                       builder: ManifestBuilderService,
                                       app_values: Values,
                                       deployment_as_dict: dict):
        manifest = builder.render_deployment_manifest(app_values)
        assert yaml.safe_load(manifest) == deployment_as_dict

    def test_build_service_manifest(self,
                                    builder: ManifestBuilderService,
                                    app_values: Values,
                                    service_as_dict: dict):
        manifest = builder.render_service_manifest(app_values)
        assert yaml.safe_load(manifest) == service_as_dict

    def test_manifests_endpoint(self,
                                fastapi_test_client: TestClient,
                                deployment_as_dict: dict,
                                service_as_dict: dict):
        response = fastapi_test_client.post(
                "/manifests/render",
                json={
                    "app": {
                        "name": "my-app",
                        "image": "my-image:latest",
                        "port": 80,
                        "service": {
                            "name": "my-service"
                        }
                    }
                }
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Manifests rendered"
        assert response_data["deployment"] == deployment_as_dict
        assert response_data["service"] == service_as_dict

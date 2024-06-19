from copy import deepcopy
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from babyhelm.schemas.manifest_builder import Application
from babyhelm.services.manifest_builder import ManifestBuilderService


@pytest.fixture()
def builder() -> ManifestBuilderService:
    return ManifestBuilderService(Path("babyhelm/templates"))


@pytest.fixture()
def application_values_as_dict():
    return {
        "name": "some-app",
        "image": "some-image:latest",
        "ports": {
            "port": 80,
            "targetPort": 8000
        },
        "envs": [
            {
                "name": "SOME_ENV",
                "value": "SOME_VALUE"
            }
        ]
    }


@pytest.fixture()
def application_values(application_values_as_dict) -> Application:
    return Application.model_validate(application_values_as_dict)


@pytest.fixture()
def render_results():
    return {
        "deployment": {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": "some-app-deployment"
            },
            "spec": {
                "strategy": {
                    "type": "RollingUpdate",
                    "rollingUpdate": {
                        "maxSurge": 1,
                        "maxUnavailable": 1
                    }
                },
                "selector": {
                    "matchLabels": {
                        "app": "some-app"
                    }
                },
                "replicas": 2,
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": "some-app-container",
                                "image": "some-image:latest",
                                "ports": [
                                    {
                                        "containerPort": 8000
                                    }
                                ],
                                "env": [
                                    {
                                        "name": "SOME_ENV",
                                        "value": "SOME_VALUE"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        },
        "service": {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": "some-app-svc",
                "labels": {
                    "app": "some-app"
                }
            },
            "spec": {
                "type": "LoadBalancer",
                "loadBalancerClass": "tailscale",
                "ports": [
                    {
                        "port": 80,
                        "targetPort": 8000
                    }
                ],
                "selector": {
                    "app": "some-app"
                }
            }
        },
        "hpa": {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {
                "name": "some-app-autoscaler"
            },
            "spec": {
                "maxReplicas": 5,
                "metrics": [
                    {
                        "resource": {
                            "name": "cpu",
                            "target": {
                                "averageUtilization": 30,
                                "type": "Utilization"
                            }
                        },
                        "type": "Resource"
                    },
                    {
                        "resource": {
                            "name": "memory",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": 250
                            }
                        },
                        "type": "Resource"
                    }
                ],
                "minReplicas": 2,
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": "some-app-deployment"
                }
            }
        }
    }


@pytest.fixture()
def invalid_application_values_as_dict(application_values_as_dict):
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
    def test_build_manifests(self,
                             builder: ManifestBuilderService,
                             application_values: Application,
                             render_results: dict,
                             manifest_type):
        manifests = builder.render_application(application_values)
        assert getattr(manifests, manifest_type) == render_results.get(manifest_type)

    def test_manifests_endpoint(self,
                                fastapi_test_client: TestClient,
                                application_values_as_dict: dict,
                                render_results: dict):
        response = fastapi_test_client.post(
                "/manifests/render",
                json=application_values_as_dict
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["deployment"] == render_results["deployment"]
        assert response_data["service"] == render_results["service"]
        assert response_data["hpa"] == render_results["hpa"]

    @pytest.mark.parametrize("invalid_input_type", ["invalid_name", "invalid_image", "invalid_env"])
    def test_manifests_endpoint_validation(self,
                                           fastapi_test_client: TestClient,
                                           application_values_as_dict: dict,
                                           render_results: dict,
                                           invalid_application_values_as_dict: dict,
                                           invalid_input_type):
        response = fastapi_test_client.post(
                "/manifests/render",
                json=invalid_application_values_as_dict[invalid_input_type]
        )
        assert response.status_code == 422

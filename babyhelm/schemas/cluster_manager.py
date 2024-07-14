from copy import deepcopy

from pydantic import BaseModel, ConfigDict, RootModel

from babyhelm.schemas.manifest_builder import Application
from babyhelm.schemas.user import USER_EXAMPLE, UserSchema

APPLICATION_EXAMPLE = {"name": "some-application", "image": "docker.io/nginx:latest"}

APPLICATION_WITH_LINK_EXAMPLE = deepcopy(APPLICATION_EXAMPLE)
APPLICATION_WITH_LINK_EXAMPLE["deployment_link"] = "https://some-link.com/my-app"

PROJECT_EXAMPLE = {
    "name": "some-project",
    "applications": [APPLICATION_EXAMPLE],
    "users": [USER_EXAMPLE],
}

APPLICATION_LOGS_EXAMPLE = {
    "pod-1": ["log-line-1", "log-line-2"],
    "pod-2": ["log-line-1", "log-line-2"],
}


class CreateApplicationRequest(BaseModel):
    application: Application


class ApplicationSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"examples": [APPLICATION_EXAMPLE]}
    )

    name: str
    image: str


class ProjectSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"examples": [PROJECT_EXAMPLE]}
    )

    name: str
    applications: list[ApplicationSchema] = []
    users: list[UserSchema] = []


class ApplicationWithLinkSchema(ApplicationSchema):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"examples": [APPLICATION_WITH_LINK_EXAMPLE]},
    )

    deployment_link: str


class ApplicationLogsSchema(RootModel):
    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"examples": [APPLICATION_LOGS_EXAMPLE]}
    )

    root: dict[str, list[str]]

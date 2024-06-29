from pydantic import BaseModel, ConfigDict

from babyhelm.schemas.manifest_builder import Application, Project
from babyhelm.schemas.user import USER_EXAMPLE, UserSchema

APPLICATION_EXAMPLE = {"name": "some-application", "image": "docker.io/nginx:latest"}

PROJECT_EXAMPLE = {
    "name": "some-project",
    "applications": [APPLICATION_EXAMPLE],
    "users": [USER_EXAMPLE],
}


class CreateApplicationRequest(BaseModel):
    application: Application
    project: Project


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

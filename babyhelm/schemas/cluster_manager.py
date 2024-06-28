from pydantic import BaseModel, Field

from babyhelm.schemas.manifest_builder import Application, Project


class CreateApplicationRequest(BaseModel):
    application: Application
    project: Project


class CreateApplicationResponse(BaseModel):
    app_link: str = Field(examples=["projectname-appname-babyhelm.com"])


class CreateProjectResponse(BaseModel):
    pass

from pydantic import BaseModel

from babyhelm.schemas.manifest_builder import Application, Project


class ApplicationRequest(BaseModel):
    application: Application
    project: Project

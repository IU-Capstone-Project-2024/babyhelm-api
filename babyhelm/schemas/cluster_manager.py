from babyhelm.schemas.manifest_builder import Application, Project
from pydantic import BaseModel


class ApplicationRequest(BaseModel):
    application: Application
    project: Project

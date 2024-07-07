from babyhelm.exceptions.base import (
    ClientError,
    ClusterManagerError,
    ConflictError,
    NotFoundError,
)


class DatabaseError(ClusterManagerError):
    def __init__(self, entity_name):
        super().__init__(f"Error creating {entity_name}")


class ClusterError(ClusterManagerError):
    def __init__(self, entity_name):
        super().__init__(f"Error creating {entity_name}")


class ForbiddenProjectName(ClientError):
    def __init__(self, project_name: str):
        super().__init__(f"project name {project_name} is forbidden")


class ProjectNameAlreadyTaken(ConflictError):
    def __init__(self, project_name: str):
        super().__init__(f"project name {project_name} is already taken")


class ApplicationNameAlreadyTaken(ConflictError):
    def __init__(self, application_name: str):
        super().__init__(f"application name {application_name} is already taken")


class ProjectNotFound(NotFoundError):
    def __init__(self):
        super().__init__("project not found")


class ApplicationsAreNotEmpty(ClientError):
    def __init__(self, project_name: str):
        super().__init__(f"project {project_name} still has deployed applications")


class ApplicationNotFound(NotFoundError):
    def __init__(self):
        super().__init__("application not found")

from babyhelm.exceptions.base import ClusterManagerError


class DatabaseError(ClusterManagerError):
    def __init__(self, entity_name):
        super().__init__(f"Error creating {entity_name}")


class ClusterError(ClusterManagerError):
    def __init__(self, entity_name):
        super().__init__(f"Error creating {entity_name}")

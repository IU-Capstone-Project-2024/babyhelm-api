class ClusterManagerError(Exception):
    """
    Custom exception class for Cluster Manager Service errors.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

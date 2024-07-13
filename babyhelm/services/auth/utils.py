from enum import Enum


class RoleEnum(Enum):
    creator = "creator"
    editor = "editor"
    viewer = "viewer"


class ActionEnum(Enum):
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    REBOOT = "reboot"
    ADD_NEW_USER = "add_new_user"


class RolePermissionsEnum(Enum):
    ...

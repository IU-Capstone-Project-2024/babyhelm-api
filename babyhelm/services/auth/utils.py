from enum import Enum


class RoleEnum(Enum):
    creator = "creator"
    editor = "editor"
    viewer = "viewer"


class ActionEnum(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    RESTART = "restart"
    ADD_NEW_USER = "add_new_user"


role_permission_dict = {
    "creator": (
        ActionEnum.CREATE.name,
        ActionEnum.READ.name,
        ActionEnum.UPDATE.name,
        ActionEnum.DELETE.name,
        ActionEnum.RESTART.name,
        ActionEnum.ADD_NEW_USER.name,
    ),
    "editor": (ActionEnum.READ.name, ActionEnum.UPDATE.name, ActionEnum.RESTART.name),
    "viewer": (ActionEnum.READ.name,),
}

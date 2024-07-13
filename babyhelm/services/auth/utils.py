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


role_permission_dict = {
    "creator": (
        ActionEnum.READ.name,
        ActionEnum.UPDATE.name,
        ActionEnum.DELETE.name,
        ActionEnum.REBOOT.name,
        ActionEnum.ADD_NEW_USER.name,
    ),
    "editor": (ActionEnum.READ.name, ActionEnum.UPDATE.name, ActionEnum.REBOOT.name),
    "viewer": (ActionEnum.READ.name,),
}

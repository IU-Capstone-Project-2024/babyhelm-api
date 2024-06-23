from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from babyhelm.models.base import Base
from babyhelm.models.project import Project
from babyhelm.models.user import User


class UserProjectAssociation(Base):
    __tablename__ = "users_projects"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    project_name: Mapped[str] = mapped_column(
        ForeignKey("projects.name"), primary_key=True
    )

    user: Mapped["User"] = relationship(back_populates="projects")
    project: Mapped["Project"] = relationship(back_populates="users")

    # TODO add role and permission on project for user

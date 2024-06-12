from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from babyhelm.models.base import Base
from babyhelm.models.user import User
from babyhelm.models.project import Project


class UserProjectAssociation(Base):
    __tablename__ = "user_project_association"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="projects")
    project: Mapped["Project"] = relationship(back_populates="users")

    # TODO add role and permission on project for user

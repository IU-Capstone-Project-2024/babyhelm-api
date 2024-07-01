from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from babyhelm.models.base import Base
from babyhelm.models.mixins import TimeStampMixin

if TYPE_CHECKING:
    from babyhelm.models import Application, User


class Project(Base, TimeStampMixin):
    """Project model."""

    __tablename__ = "projects"
    name: Mapped[str] = mapped_column(primary_key=True)

    # many-to-many
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="users_projects",
        back_populates="projects",
    )

    applications: Mapped[list["Application"]] = relationship(back_populates="project")

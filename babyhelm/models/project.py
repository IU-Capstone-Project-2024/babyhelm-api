from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from babyhelm.models.base import Base
from babyhelm.models.mixins import TimeStampMixin, IdMixin


class Project(Base, TimeStampMixin, IdMixin):
    """Project model."""

    __tablename__ = "projects"
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    # many-to-many
    users: Mapped[list["UserProjectAssociation"]] = relationship(back_populates="projects")

    applications: Mapped[list["Application"]] = relationship("Application", back_populates="project")

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from babyhelm.models.base import Base
from babyhelm.models.mixins import IdMixin, TimeStampMixin
from babyhelm.models.project import Project


class Application(Base, TimeStampMixin, IdMixin):
    """Application model."""

    __tablename__ = "applications"
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False, unique=True
    )
    # TODO add app-related configuration info

    project: Mapped["Project"] = relationship(back_populates="applications")

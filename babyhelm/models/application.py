from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from babyhelm.models.base import Base
from babyhelm.models.mixins import IdMixin, TimeStampMixin
from babyhelm.models.project import Project


class Application(Base, TimeStampMixin):
    """Application model."""

    __tablename__ = "applications"
    name: Mapped[str] = mapped_column(nullable=False)
    project_name: Mapped[int] = mapped_column(
        ForeignKey("projects.name"), nullable=False
    )
    image: Mapped[str] = mapped_column(nullable=False)

    project: Mapped["Project"] = relationship(back_populates="applications")

    __table_args__ = (PrimaryKeyConstraint("name", "project_name"),)

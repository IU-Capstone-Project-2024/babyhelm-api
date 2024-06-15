from sqlalchemy.orm import Mapped, mapped_column, relationship

from babyhelm.models.base import Base
from babyhelm.models.mixins import TimeStampMixin, IdMixin


class User(Base, TimeStampMixin, IdMixin):
    """User model."""

    __tablename__ = "users"
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped[list["UserProjectAssociation"]] = relationship(back_populates="user")

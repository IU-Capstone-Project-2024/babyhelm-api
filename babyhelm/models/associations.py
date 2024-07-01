from sqlalchemy import Column, ForeignKey, Table

from babyhelm.models.base import Base

users_projects = Table(
    "users_projects",
    Base.metadata,
    Column(
        "project_name",
        ForeignKey("projects.name", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

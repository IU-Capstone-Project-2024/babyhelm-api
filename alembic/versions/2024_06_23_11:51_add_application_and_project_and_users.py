"""add_application_and_project_and_users

Revision ID: f71bd58788a0
Revises:
Create Date: 2024-06-23 11:51:03.373678+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f71bd58788a0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "projects",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )
    op.create_table(
        "users",
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "applications",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("project_name", sa.String(), nullable=False),
        sa.Column("image", sa.String(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_name"],
            ["projects.name"],
        ),
        sa.PrimaryKeyConstraint("name", "project_name"),
    )
    op.create_table(
        "users_projects",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("project_name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_name"],
            ["projects.name"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "project_name"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users_projects")
    op.drop_table("applications")
    op.drop_table("users")
    op.drop_table("projects")
    # ### end Alembic commands ###
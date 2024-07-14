"""add user role to users_projects

Revision ID: 8383de86fbd0
Revises: 110317721d0c
Create Date: 2024-07-10 17:29:04.079063+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = "8383de86fbd0"
down_revision: Union[str, None] = "110317721d0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

role_enum = ENUM('creator', 'editor', 'viewer', name='roleenum')


def upgrade() -> None:
    role_enum.create(op.get_bind())
    op.add_column(
        "users_projects",
        sa.Column(
            "role",
            sa.Enum("creator", "editor", "viewer", name="roleenum"),
            nullable=True,
        ),
    )

    op.execute("UPDATE users_projects SET role = 'creator' WHERE role IS NULL")
    op.alter_column("users_projects", "role", nullable=False)


def downgrade() -> None:
    op.drop_column("users_projects", "role")
    role_enum.drop(op.get_bind())

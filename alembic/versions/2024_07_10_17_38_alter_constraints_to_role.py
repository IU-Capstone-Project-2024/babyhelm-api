"""alter constraints to role

Revision ID: 87bb66994e0c
Revises: 8383de86fbd0
Create Date: 2024-07-10 17:38:25.913227+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "87bb66994e0c"
down_revision: Union[str, None] = "8383de86fbd0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users_projects",
        "role",
        existing_type=postgresql.ENUM("creator", "editor", "viewer", name="roleenum"),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "users_projects",
        "role",
        existing_type=postgresql.ENUM("creator", "editor", "viewer", name="roleenum"),
        nullable=True,
    )

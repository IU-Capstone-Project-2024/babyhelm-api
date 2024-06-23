"""rename password

Revision ID: 56a540109b2f
Revises: 89db4ac8caff
Create Date: 2024-06-23 19:53:06.699659+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "56a540109b2f"
down_revision: Union[str, None] = "89db4ac8caff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("hashed_password", sa.String(), nullable=False))
    op.drop_column("users", "password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("password", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("users", "hashed_password")
    # ### end Alembic commands ###
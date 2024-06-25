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
    op.alter_column("users", "password", new_column_name="hashed_password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", "hashed_password", new_column_name="password")
    # ### end Alembic commands ###
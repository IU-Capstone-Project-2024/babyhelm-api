"""Add workloads in applications

Revision ID: 110317721d0c
Revises: 56a540109b2f
Create Date: 2024-06-25 14:48:16.294018+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "110317721d0c"
down_revision: Union[str, None] = "56a540109b2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
            "applications", sa.Column("service_name", sa.String(), nullable=True)
    )
    op.add_column(
            "applications", sa.Column("deployment_name", sa.String(), nullable=True)
    )
    op.add_column(
            "applications", sa.Column("autoscaler_name", sa.String(), nullable=True)
    )
    # ### end Alembic commands ###
    op.execute("UPDATE applications SET service_name = name || '-svc' WHERE service_name IS NULL")
    op.execute("UPDATE applications SET deployment_name = name || '-deployment' WHERE service_name IS NULL")
    op.execute("UPDATE applications SET autoscaler_name = name || '-hpa' WHERE service_name IS NULL")

    op.alter_column("applications", "service_name", nullable=False)
    op.alter_column("applications", "deployment_name", nullable=False)
    op.alter_column("applications", "autoscaler_name", nullable=False)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("applications", "autoscaler_name")
    op.drop_column("applications", "deployment_name")
    op.drop_column("applications", "service_name")
    # ### end Alembic commands ###

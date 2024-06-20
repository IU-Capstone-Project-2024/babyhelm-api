import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class TimeStampMixin:
    created: Mapped[datetime.datetime] = mapped_column(default=sa.func.now())
    modified: Mapped[datetime.datetime] = mapped_column(
        default=sa.func.now(), onupdate=sa.func.now()
    )


class IdMixin:
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)

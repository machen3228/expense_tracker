from typing import TYPE_CHECKING

from sqlalchemy import UUID
from sqlalchemy import LargeBinary
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from tracker.infrastructure.database.models.base import BaseORM

if TYPE_CHECKING:
    from tracker.domain.entities.person import PersonId


class PersonORM(BaseORM):
    __tablename__ = "persons"

    id: Mapped[PersonId] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(
        String(30),
        unique=True,
    )
    password_hash: Mapped[bytes] = mapped_column(LargeBinary)

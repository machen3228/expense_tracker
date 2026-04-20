from typing import TYPE_CHECKING
from typing import NoReturn

from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from tracker.application.errors.base import OperationFailedError
from tracker.application.interfaces.transaction_manager import ITransactionManager
from tracker.domain.errors.base import AlreadyExistsError
from tracker.domain.errors.base import NotFoundError
from tracker.domain.errors.base import ValidationError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SATransactionManager(ITransactionManager):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as e:
            self._handle_exception(e)

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as e:
            self._handle_exception(e)

    @staticmethod
    def _handle_exception(exception: SQLAlchemyError) -> NoReturn:
        if isinstance(exception, IntegrityError):
            orig_error: str = str(exception.orig).lower()
            if "uq_" in orig_error or "pk_" in orig_error:
                raise AlreadyExistsError from exception
            if "fk_" in orig_error:
                raise NotFoundError from exception
            if "ck_" in orig_error:
                raise ValidationError from exception
        raise OperationFailedError from exception

from tracker.domain.errors import AppError


class ApplicationError(AppError):
    pass


class OperationFailedError(ApplicationError):
    pass


class UnexpectedError(ApplicationError):
    pass

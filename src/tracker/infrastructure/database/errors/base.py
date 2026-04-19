from tracker.application.errors.base import ApplicationError


class InfrastructureError(ApplicationError):
    pass


class DataMapperError(InfrastructureError):
    pass

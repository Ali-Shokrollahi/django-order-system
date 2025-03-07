from rest_framework import status


class ServiceException(Exception):
    """Base exception for service layer errors."""

    def __init__(self, message: str, status_code: int = None, extra: dict = None):
        self.message = message
        self.status_code = status_code
        self.extra = extra or {}
        super().__init__(message)


class ResourceNotFoundException(ServiceException):
    """Raised when a requested resource is not found."""

    def __init__(self, resource_name="Resource", extra: dict = None):
        message = f"{resource_name} not found"
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND, extra=extra)


class ResourceAlreadyExistsException(ServiceException):
    """Raised when attempting to create a resource that already exists."""

    def __init__(self, resource_name="Resource", identifier=None, extra: dict = None):
        message = (
            f"{resource_name} already exists"
            if not identifier
            else f"{resource_name} with this {identifier} already exists"
        )
        super().__init__(message, status_code=status.HTTP_409_CONFLICT, extra=extra)


# External Service or Dependency Exceptions
class ExternalServiceException(ServiceException):
    """Raised when an external service fails."""

    def __init__(self, service_name="External service", extra: dict = None):
        message = f"{service_name} unavailable"
        super().__init__(
            message, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, extra=extra
        )

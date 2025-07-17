"""Custom exceptions for the EMT Madrid domain."""

from typing import Optional, Dict, Any


class EMTError(Exception):
    """Base exception for all EMT API related errors."""

    pass


class AuthenticationError(EMTError):
    """Raised when there is an authentication error with the EMT API."""

    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when the provided credentials are invalid."""

    pass


class APIResponseError(EMTError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message)


class StopNotFoundError(APIResponseError):
    """Raised when the specified bus stop is not found."""

    pass


class APILimitExceededError(APIResponseError):
    """Raised when the API limit is exceeded."""

    pass

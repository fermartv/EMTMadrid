"""Custom exceptions for the EMT Madrid domain."""

from typing import Optional


class EMTError(Exception):
    """Base exception for all EMT API related errors."""

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(message or "An unknown EMT error occurred")


class AuthenticationError(EMTError):
    """Raised when there is an authentication error with the EMT API."""

    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when the provided credentials are invalid."""

    pass


class APIResponseError(EMTError):
    """Raised when the API returns an error response."""

    pass


class StopNotFoundError(APIResponseError):
    """Raised when the specified bus stop is not found."""

    def __init__(
        self, stop_id: Optional[int] = None, message: Optional[str] = None
    ) -> None:
        default_message = (
            f"Stop {stop_id} not found" if stop_id is not None else "Stop not found"
        )
        super().__init__(message or default_message)
        self.stop_id = stop_id


class APILimitExceededError(APIResponseError):
    """Raised when the API limit is exceeded."""

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(message or "API rate limit exceeded")


class ArrivalsNotFoundError(APIResponseError):
    """Raised when the specified bus stop arrivals are not found."""

    def __init__(
        self, stop_id: Optional[int] = None, message: Optional[str] = None
    ) -> None:
        default_message = (
            f"No arrivals found for stop {stop_id}"
            if stop_id is not None
            else "No arrivals found"
        )
        super().__init__(message or default_message)
        self.stop_id = stop_id

class NoVariableError(Exception):
    """Variable missing."""


class EndpointNotAvailable(Exception):
    """Endpoint is not available."""


class UnknownHomeworkStatus(Exception):
    """Unknow homework status."""


class SendMessageError(Exception):
    """Message send error."""

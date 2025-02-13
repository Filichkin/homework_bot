class NoVariableError(Exception):
    """Variable missing."""


class EndpointNotAvailable(Exception):
    """Endpoint is not available."""


class UnknownHomeworkStatus(Exception):
    """Unknow homework status."""


class JsonError(Exception):
    """JSON decode error."""


class SendMessageError(Exception):
    """Message send error."""

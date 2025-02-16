class NoVariableError(Exception):
    """Variable missing."""

    pass


class EndpointNotAvailable(Exception):
    """Endpoint is not available."""

    pass


class UnknownHomeworkStatus(Exception):
    """Unknow homework status."""

    pass


class JsonError(Exception):
    """JSON decode error."""

    pass


class CurrentDateStatus(Exception):
    """Current date status error."""

    pass

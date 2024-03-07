class AuthorizationError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class NotFoundError(ValueError):
    pass


class ValidationError(ValueError):
    pass


class ResourceExistsError(ValueError):
    pass

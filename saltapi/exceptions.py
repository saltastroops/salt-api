class AuthorizationError(Exception):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message)


class AuthenticationError(Exception):
    pass


class NotFoundError(ValueError):
    pass


class ValidationError(ValueError):
    pass


class ResourceExistsError(ValueError):
    pass


class SSDAError(Exception):
    def __init__(self, message: str = "Failed to update SAAO SALT Data Archive."):
        self.message = message
        super().__init__(self.message)


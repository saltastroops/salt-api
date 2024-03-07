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


class InactiveUserError(Exception):
    def __init__(self, message="User account is not active. Please contact SALT Help for assistance."):
        self.message = message
        super().__init__(self.message)

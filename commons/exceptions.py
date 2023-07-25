from commons.constants.api_error_code import APIErrorCode
from rest_framework import status
from rest_framework.exceptions import APIException

class NotFoundException(APIException):
    """
    Class for not found exception.
    """

    status_code = status.HTTP_404_NOT_FOUND
    default_code = APIErrorCode.HTTP_404_NOT_FOUND

    def __init__(self, data=None):
        if data is not None:
            self.data = data

        super().__init__(code=self.default_code)

class ValidationException(APIException):
    """
    Class for validation exception.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_code = APIErrorCode.HTTP_422_VALIDATION_ERROR

    def __init__(self, data=None):
        if data is not None:
            self.data = data

        super().__init__(code=self.default_code)

class ForbiddenException(APIException):
    """
    Class for forbidden exception.
    """

    status_code = status.HTTP_403_FORBIDDEN
    default_code = APIErrorCode.HTTP_403_FORBIDDEN

    def __init__(self, data=None):
        if data is not None:
            self.data = data

        super().__init__(code=self.default_code)

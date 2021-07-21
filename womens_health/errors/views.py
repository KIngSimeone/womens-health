from enum import Enum, IntEnum
from .models import Error
from django.db import IntegrityError


class ErrorCodes(IntEnum):
    GENERIC_ERROR = 0
    UNAUTHENTICATED_REQUEST = 1
    UNAUTHORIZED_REQUEST = 2
    MISSING_FIELDS = 3
    USER_ALREADY_EXISTS = 4
    USER_CREATION_FAILED = 5


# base error
def getError(code, defaultMessage):
    try:
        _, _ = Error.objects.get_or_create(
            code=code, description=defaultMessage)

        return {'errorCode': code, 'message': defaultMessage}

    except IntegrityError:
        return {'errorCode': code, 'message': defaultMessage}

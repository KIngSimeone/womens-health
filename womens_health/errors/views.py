from enum import Enum, IntEnum
from .models import Error
from django.db import IntegrityError


class ErrorCodes(IntEnum):
    GENERIC_ERROR = 0
    UNAUTHENTICATED_REQUEST = 1
    UNAUTHORIZED_REQUEST = 2
    MISSING_FIELDS = 3

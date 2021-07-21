import json
import logging
from errors.views import ErrorCodes
from api_utils.views import (
    badRequestResponse, request_response, resourceConflictResponse, internalServerErrorResponse,
    unAuthenticatedResponse,
    unAuthorizedResponse, successResponse, resourceNotFoundResponse,
)
from api_utils.validators import (
    validateKeys
)
from .utils import (
    createPatient
)
# Get an instance of a logger
logger = logging.getLogger(__name__)
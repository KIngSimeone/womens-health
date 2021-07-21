import json
import logging

from api_utils.views import (badRequestResponse, internalServerErrorResponse,
                             requestResponse, resourceConflictResponse,
                             resourceNotFoundResponse, successResponse,
                             unAuthenticatedResponse, unAuthorizedResponse)
from data_transformer.views import dateIsISO
from django.conf import settings
from errors.views import ErrorCodes
from Users.utils import getUserByAccessToken

# Get an instance of a logger
logger = logging.getLogger(__name__)

def createCycles(request):
    """create cycle api endpoint"""
    body = json.loads(request.body)

    token = request.headers.get('Token')
    if token is None:
        return requestResponse(badRequestResponse, ErrorCodes.INVALID_CREDENTIALS,
                                "Token is missing in the request headers")

    # get user with access token
    user = getUserByAccessToken(token)
    if user is None:
        return requestResponse(unAuthenticatedResponse, ErrorCodes.UNAUTHENTICATED_REQUEST,
                                "Your session has expired. Please login.")

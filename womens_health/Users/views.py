import json
import logging
from django.conf import settings
from errors.views import ErrorCodes
from api_utils.views import (
    badRequestResponse, resourceConflictResponse, internalServerErrorResponse,
    unAuthenticatedResponse, requestResponse,
    unAuthorizedResponse, successResponse, resourceNotFoundResponse,
)
from api_utils.validators import (
    validateKeys, validateInputFormat, validateThatStringIsEmpty
)
from .utils import (
    createPatient, getPatientByInputs
)
from data_transformer.views import dateIsISO
from data_transformer.json_serializer import transformPatient
# Get an instance of a logger
logger = logging.getLogger(__name__)


def provisionPatient(request):
    """api for creating patient"""
    body = json.loads(request.body)

    # verify that the calling user has a valid secret key
    secret = request.headers.get('Secret')
    if secret is None:
        return requestResponse(unAuthorizedResponse, 
                                ErrorCodes.INVALID_CREDENTIALS, 
                                "Secret is missing in the request headers")
    elif secret != settings.ROOT_SECRET:
        return requestResponse(unAuthorizedResponse,
                                ErrorCodes.INVALID_CREDENTIALS,
                                "Invalid Secret specified in the request headers")

    # check if required fields are present in request payload
    missing_keys = validateKeys(payload=body, requiredKeys=['firstName', 'lastName', 'email', 'phone', 'password', 'birthday'])
    if missing_keys:
        return requestResponse(
            badRequestResponse, ErrorCodes.MISSING_FIELDS,
            f"The following key(s) are missing in the request "
            f"payload: {missing_keys}")

    firstname = body['firstName'].strip()
    lastname = body['lastName'].strip()
    phone = body['phone'].strip()
    email = body['email']
    password = body['password']
    birthday = body['birthday']

    # validate input format
    valid_input, msg = validateInputFormat(
        (firstname, lastname), email, phone)
    if not valid_input:
        return requestResponse(badRequestResponse, ErrorCodes.GENERIC_ERROR, msg)

    # check if Password is not empty
    if not validateThatStringIsEmpty(password):
        return requestResponse(badRequestResponse, ErrorCodes.GENERIC_ERROR, "Password cannot be empty")

    # check if inputs already exists
    valid_input, msg = getPatientByInputs(phone, email)
    if not valid_input:
        return requestResponse(resourceConflictResponse, ErrorCodes.USER_ALREADY_EXISTS, msg)

    if not dateIsISO(birthday):
        return requestResponse(badRequestResponse, ErrorCodes.GENERIC_ERROR, "Date of birth is invalid or empty - It must be in YYYY-MM-DD format")

    # create the patient
    patient, msg = createPatient(firstname, lastname, email, phone, password, birthday)
    if not patient:
        return requestResponse(internalServerErrorResponse, 
                              ErrorCodes.USER_CREATION_FAILED, msg)

    return successResponse(message="Account successfully created", body=transformPatient(patient))

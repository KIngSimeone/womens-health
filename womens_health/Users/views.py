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
    authenticateUser, createPatient, getPatientByInputs, generateUserAccessToken,
    authenticateUser
)
from data_transformer.views import dateIsISO
from data_transformer.json_serializer import transformPatient
# Get an instance of a logger
logger = logging.getLogger(__name__)


def login(request):
    """login api endpoint"""
    body = json.loads(request.body)

    # verify that the calling user has a valid secret key
    secret = request.headers.get('Secret')
    if secret is None:
        return requestResponse(badRequestResponse, ErrorCodes.INVALID_CREDENTIALS, "Secret is missing in the request headers")
    if secret != settings.ROOT_SECRET:
        requestResponse(badRequestResponse, ErrorCodes.INVALID_CREDENTIALS, "Invalid Secret specified in the request headers")

    # check if required fields are present in request payload
    missing_keys = validateKeys(payload=body, requiredKeys=['userIdentity', 'password'])
    if missing_keys:
        return requestResponse(badRequestResponse,
                                ErrorCodes.MISSING_FIELDS, "The following key(s) are missing in the request "
                                f"payload: {missing_keys}")
    user_identity = body['userIdentity'].strip()
    password = body['password']

    # check if ID is not empty
    if not validateThatStringIsEmpty(user_identity):
        return requestResponse(badRequestResponse, ErrorCodes.GENERIC_ERROR, "User Identity cannot be empty")

    # check if password is not empty
    if not validateThatStringIsEmpty(password):
        return requestResponse(badRequestResponse, ErrorCodes.GENERIC_ERROR, "Password field cannot be empty")

    # Authenticate user
    user = authenticateUser(user_identity, password)
    if user is None:
        return requestResponse(unAuthenticatedResponse, ErrorCodes.INVALID_CREDENTIALS, "Invalid Credentials")

    # get User access token
    access_token, msg = generateUserAccessToken(user)
    if access_token is None:
        requestResponse(internalServerErrorResponse, ErrorCodes.GENERIC_ERROR, msg)

    return successResponse(message="successfully authenticated", body=userLoginResponse(user, access_token))


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
        return requestResponse(
            badRequestResponse, ErrorCodes.GENERIC_ERROR,
            "Date of birth is invalid or empty - It must be in YYYY-MM-DD format")

    # create the patient
    patient, msg = createPatient(firstname, lastname, email, phone, password, birthday)
    if not patient:
        return requestResponse(internalServerErrorResponse,
                               ErrorCodes.USER_CREATION_FAILED, msg)

    return successResponse(message="Account successfully created", body=transformPatient(patient))

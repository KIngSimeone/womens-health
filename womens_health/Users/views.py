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
    validateKeys, validateInputFormat
)
from .utils import (
    createPatient
)
from data_transformer.views import dateIsISO
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
    missing_keys = validateKeys(payload=body, requiredKeys=['firstname', 'lastname', 'email', 'phone', 'password', 'birthday'])
    if missing_keys:
        return requestResponse(
            badRequestResponse, ErrorCodes.MISSING_FIELDS,
            f"The following key(s) are missing in the request "
            f"payload: {missing_keys}")

    firstname = body['firstname'].strip()
    lastname = body['lastname'].strip()
    phone = body['phone'].strip()
    email = body['email']
    password = body['password']
    birthday = body['birthday']

    # validate input format
    valid_input, msg = validateInputFormat(
        (firstname, lastname, username), email, phone)
    if not valid_input:
        return requestResponse(badRequestResponse, ErrorCodes.GENERIC_ERROR, msg)

    # check if Password is not empty
    if not validateThatStringIsEmpty(password):
        return requestResponse(badRequestResponse, ErrorCodes.GENERIC_ERROR, "Password cannot be empty")

    # check if inputs already exists
    valid_input, msg = get_staff_by_inputs(username, phone, email)
    if not valid_input:
        return requestResponse(resourceConflictResponse, ErrorCodes.USER_ALREADY_EXISTS, msg)

    # check if company exists
    check_company, err = retrieve_company_by_id(company.id)
    if check_company is None:
        return requestResponse(resourceNotFoundResponse, ErrorCodes.COMPANY_DOES_NOT_EXIST, str(err))

    # create the staff
    staff, msg = create_staff_record(firstname, lastname, username, email, phone, password, company, staff_role)
    if not staff:
        return requestResponse(internalServerErrorResponse, ErrorCodes.USER_CREATION_FAILED, msg)

    return successResponse(message="Account successfully created", body=transformStaff(staff))

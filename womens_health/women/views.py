import json
import logging
from re import I

from api_utils.views import (badRequestResponse, internalServerErrorResponse,
                             requestResponse, resourceConflictResponse,
                             resourceNotFoundResponse, successResponse,
                             unAuthenticatedResponse, unAuthorizedResponse)
from data_transformer.views import dateIsISO
from django.conf import settings
from errors.views import ErrorCodes
from Users.utils import getUserByAccessToken
from api_utils.validators import validateKeys
from .utils import (
    createPeriodInfo, updatePeriodInfo, getPeriodinfoByPatient, checkDateinRange
)
from .models import PeriodInfo
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import pytz

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

    # check if required fields are present in request payload
    missing_keys = validateKeys(payload=body, requiredKeys=[
                                'Last_period_date', 'Cycle_average', 'Period_average', 'Start_date', 'end_date'])
    if missing_keys:
        return requestResponse(
            badRequestResponse, ErrorCodes.MISSING_FIELDS,
            f"The following key(s) are missing in the request "
            f"payload: {missing_keys}")

    last_period_date = body['Last_period_date']
    cycle_average = body['Cycle_average']
    period_average = body['Period_average']
    start_date = body['Start_date']
    end_date = body['end_date']

    # validate last_period_date format
    if not dateIsISO(last_period_date):
        return requestResponse(
            badRequestResponse, ErrorCodes.GENERIC_ERROR,
            "Last period date is invalid or empty - It must be in YYYY-MM-DD format")

    # get logged in patients period info
    patientPeriodInfo = getPeriodinfoByPatient(user)
    if not patientPeriodInfo:
        patientPeriodInfo, msg = createPeriodInfo(user, cycle_average, period_average,
                                                  last_period_date)
        if not patientPeriodInfo:
            requestResponse(internalServerErrorResponse, ErrorCodes.GENERIC_ERROR, msg)
    
    updatedpatientPeriodInfo, msg = updatePeriodInfo(patientPeriodInfo, cycle_average, period_average,
                                                    last_period_date)
    if not updatedpatientPeriodInfo:
        return requestResponse(internalServerErrorResponse, ErrorCodes.GENERIC_ERROR, msg)

    delta = relativedelta(days=cycle_average)
    parsed_last_period_date =  pytz.utc.localize(parse(last_period_date))
    next_period_date = parsed_last_period_date + delta
    parsed_start_date = pytz.utc.localize(parse(start_date))
    parsed_end_date = pytz.utc.localize(parse(end_date))

    print(next_period_date)
    correct_date = checkDateinRange(parsed_start_date, parsed_end_date,
                                    next_period_date, cycle_average, period_average)

    total_no_of_days = parsed_end_date - correct_date
    delta_total_no_of_days = total_no_of_days.days

    total_created_cycles = delta_total_no_of_days / cycle_average + period_average    

    data = {
        "total_created_cycles": round(total_created_cycles),
        "totalDays": delta_total_no_of_days,
        "next_period_date": correct_date
    }

    return successResponse(message="success", body=data)

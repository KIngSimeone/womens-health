import json
import logging
from re import I

from api_utils.views import (badRequestResponse, errorResponse, internalServerErrorResponse,
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

    # validate start_date format
    if not dateIsISO(start_date):
        return requestResponse(
            badRequestResponse, ErrorCodes.GENERIC_ERROR,
            "Start date is invalid or empty - It must be in YYYY-MM-DD format")

     # validate start_date format
    if not dateIsISO(end_date):
        return requestResponse(
            badRequestResponse, ErrorCodes.GENERIC_ERROR,
            "End date is invalid or empty - It must be in YYYY-MM-DD format")

    # get logged in patients period info
    patientPeriodInfo = getPeriodinfoByPatient(user)
    if not patientPeriodInfo:
        # create a new patient periodinfo
        patientPeriodInfo, msg = createPeriodInfo(user, cycle_average, period_average,
                                                  last_period_date, start_date, end_date)
        if not patientPeriodInfo:
            requestResponse(internalServerErrorResponse, ErrorCodes.GENERIC_ERROR, msg)

    # update patient period info
    updatedpatientPeriodInfo, msg = updatePeriodInfo(patientPeriodInfo, cycle_average, period_average,
                                                     last_period_date, start_date, end_date)
    if not updatedpatientPeriodInfo:
        return requestResponse(internalServerErrorResponse, ErrorCodes.GENERIC_ERROR, msg)

    # converts cycle_avegare to relative delta object
    delta = relativedelta(days=cycle_average)

    # converts dates from string to date objects
    parsed_last_period_date = pytz.utc.localize(parse(last_period_date))
    next_period_date = parsed_last_period_date + delta
    parsed_start_date = pytz.utc.localize(parse(start_date))
    parsed_end_date = pytz.utc.localize(parse(end_date))

    # checks if current period next date is in given range if not gets correct date
    correct_start_date = checkDateinRange(parsed_start_date, parsed_end_date,
                                          next_period_date, cycle_average, period_average)

    # get total no_of days in range and convert to day object
    total_no_of_days = parsed_end_date - correct_start_date
    delta_total_no_of_days = total_no_of_days.days

    # get total created cycles
    total_created_cycles = delta_total_no_of_days / cycle_average + period_average

    data = {
        "total_created_cycles": round(total_created_cycles)
    }

    return successResponse(message="success", body=data)


def cycleEvent(request):
    token = request.headers.get('Token')
    if token is None:
        return requestResponse(badRequestResponse, ErrorCodes.INVALID_CREDENTIALS,
                               "Token is missing in the request headers")

    # get user with access token
    user = getUserByAccessToken(token)
    if user is None:
        return requestResponse(unAuthenticatedResponse, ErrorCodes.UNAUTHENTICATED_REQUEST,
                               "Your session has expired. Please login.")

    given_date = request.GET.get('date')

    # validate last_period_date format
    if not dateIsISO(given_date):
        return requestResponse(
            badRequestResponse, ErrorCodes.GENERIC_ERROR,
            "Given date is invalid or empty - It must be in YYYY-MM-DD format")

    patientPeriodInfo = getPeriodinfoByPatient(user)
    if not patientPeriodInfo:
        return requestResponse(resourceNotFoundResponse, ErrorCodes.GENERIC_ERROR,
                               "PeriodInfo not found")
    parsed_given_date = pytz.utc.localize(parse(given_date)).date()

    start_date = patientPeriodInfo.start_date
    end_date = patientPeriodInfo.end_date
    cycle_average = patientPeriodInfo.cycle_average
    last_period_date = patientPeriodInfo.last_period_date
    period_average = patientPeriodInfo.period_average

    if not start_date <= parsed_given_date <= end_date:
        return requestResponse(badRequestResponse,
                               ErrorCodes.GENERIC_ERROR,
                               "Given date not in set date date range")

    delta = relativedelta(days=int(cycle_average))
    next_period_date = last_period_date + delta

    correct_start_date = checkDateinRange(start_date, end_date,
                                          next_period_date, cycle_average, period_average)

    periodCycles = list()
    while correct_start_date < end_date:
        delta = relativedelta(days=int(period_average))
        delta_cycle_average = relativedelta(days=int(cycle_average))
        full_cycle_delta = relativedelta(days=int(cycle_average) + int(period_average))
        period_end_date = correct_start_date + delta
        full_cycle_end = correct_start_date + full_cycle_delta
        ovulation_date = correct_start_date + delta_cycle_average / 2
        delta_fertility = relativedelta(days=4)
        fertility_window_start = ovulation_date - delta_fertility
        fertility_window_end = ovulation_date + delta_fertility
        delta_ovulation = relativedelta(days=1)
        pre_ovulation_window_start = period_end_date + delta_ovulation
        pre_ovulation_window_end = fertility_window_start - delta_ovulation
        post_ovulation_window_start = fertility_window_end + delta_ovulation
        post_ovulation_window_end = full_cycle_end - delta_ovulation
        periodCycles.append({
            "start_date": correct_start_date,
            "end_date": period_end_date,
            "full_cycle_end": full_cycle_end,
            "ovulation_date": ovulation_date,
            "fertility_window_start": fertility_window_start,
            "fertility_window_end": fertility_window_end,
            "pre_ovulation_window_start": pre_ovulation_window_start,
            "pre_ovulation_window_end": pre_ovulation_window_end,
            "post_ovulation_window_start": post_ovulation_window_start,
            "post_ovulation_window_end": post_ovulation_window_end

        })
        correct_start_date = period_end_date + delta_cycle_average
    event = ""
    for cycle in periodCycles:
        dict_start_date = cycle['start_date']
        dict_end_date = cycle['end_date']
        dict_ovulation_date = cycle['ovulation_date']
        dict_fertility_window_start = cycle['fertility_window_start']
        dict_fertility_window_end = cycle['fertility_window_end']
        dict_pre_ovulation_window_start = cycle['pre_ovulation_window_start']
        dict_pre_ovulation_window_end = cycle['pre_ovulation_window_end']
        dict_post_ovulation_window_start = cycle['post_ovulation_window_start']
        dict_post_ovulation_window_end = cycle['post_ovulation_window_end']

        if dict_start_date <= parsed_given_date <= dict_end_date:
            event = "period_cycle"
            break

        elif parsed_given_date == dict_ovulation_date:
            event = "ovulate_date"
            break

        elif dict_fertility_window_start <= parsed_given_date <= dict_fertility_window_end:
            event = "fertility_window"
            break
        
        elif dict_pre_ovulation_window_start <= parsed_given_date <= dict_pre_ovulation_window_end:
            event = "pre_ovulation_window"
            break
    
        elif dict_post_ovulation_window_start <= parsed_given_date <= dict_post_ovulation_window_end:
            event = "post_ovulation_window"
            break

    data = {
        "given_date": given_date,
        "event": event
    }
    return successResponse(message="success", body=data)

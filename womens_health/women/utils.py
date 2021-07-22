import logging
import uuid
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import relativedelta

from .models import PeriodInfo

# Get an instance of a logger
logger = logging.getLogger(__name__)

def createPeriodInfo(patient, cycle_average, period_average, last_period_date):
    """creating new period info"""
    try:
        periodInfo = PeriodInfo.objects.create(
            id=int(str(uuid.uuid4().int)[::6]),
            patient=patient,
            cycle_average=cycle_average,
            period_average=period_average,
            last_period_date=last_period_date
        )
        return periodInfo, "success"
    
    except Exception as e:
        logger.error(
            "createPeriodInfo@Error :: Error occurred while creating the period information")
        logger.error(e)
        return None, str(e)

def updatePeriodInfo(periodInfo, cycle_average, period_average, last_period_date):
    """updating period info"""
    try:
        periodInfo.cycle_average = cycle_average
        periodInfo.period_average = period_average
        periodInfo.last_period_date = last_period_date
        periodInfo.save()

        return periodInfo, "success"
    
    except Exception as e:
        logger.error(
            "updatePeriodInfo@Error :: Error occurred while updating the period information")
        logger.error(e)
        return None, str(e)

def getPeriodinfoByPatient(patient):
    """retrieve patient periodinfo"""
    try:
        periodinfo = PeriodInfo.objects.get(patient=patient)
        return periodinfo

    except ObjectDoesNotExist as e:
        logger.error("getPeriodinfoByPatient@error")
        logger.error(e)
        return None

def checkDateinRange(start_date, end_date, next_date, cycle_average, period_average):
    """Check if date in range"""
    if not start_date <= next_date >= end_date:
        while not start_date <= next_date <= end_date:
            delta = relativedelta(days=cycle_average+period_average)
            next_date = next_date + delta
            print("inside loop")
        else:
            print("outside loop")
            return next_date

    return next_date


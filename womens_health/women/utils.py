import logging
import uuid

from .models import PeriodInfo

# Get an instance of a logger
logger = logging.getLogger(__name__)

def createPeriodInfo(patient, cycle_average, period_average):
    """creating new period info"""
    try:
        periodInfo = PeriodInfo.objects.create(
            id=int(str(uuid.uuid4().int)[::6]),
            patient=patient,
            cycle_average=cycle_average,
            period_average=period_average
        )
        return periodInfo, "success"
    
    except Exception as e:
        logger.error(
            "createPeriodInfo@Error :: Error occurred while creating the period information")
        logger.error(e)
        return None, str(e)

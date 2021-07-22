import logging
from datetime import datetime

import pytz
from django.utils import timezone

# Get an instance of a logger
logger = logging.getLogger(__name__)


def dateIsISO(value):
    try:
        # can validate 2019-03-04
        if value != str(datetime.strptime(value, "%Y-%m-%d").date()):
            raise ValueError
        return True
    except ValueError:
        return False


def toUiReadableDateFormat(value):
    try:
        if value is None:
            return ""

        localizedValue = timezone.localtime(
            value, pytz.timezone('UTC'))
        return datetime.strftime(localizedValue, "%b %d, %Y %I:%M%p")
    except Exception as ex:
        logger.error(ex)
        return str(value)


def stringIsInteger(value):
    try:
        convertedValue = int(value)
        return convertedValue
    except ValueError:
        return False

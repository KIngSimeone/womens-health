import logging
import secrets
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import Patient

# Get an instance of a logger
logger = logging.getLogger(__name__)


def getExpiresAt(minutes=None):
    if not minutes:
        return (timezone.now() + timedelta(minutes=eval(settings.DURATION)))

    return (timezone.now() + timedelta(minutes=minutes))


def getPatientByPhone(phone):
    """retrieve patient by phone"""
    try:
        patient = Patient.objects.get(phone=phone)
        return patient

    except ObjectDoesNotExist as e:
        logger.error(f"Patient with phone: {phone} does not exist")
        logger.error(e)
        return None


def getPatientByEmail(email):
    """retrieve patient by email"""
    try:
        patient = Patient.objects.get(email=email)
        return patient

    except ObjectDoesNotExist as e:
        logger.error(f"Patient with email: {email} does not exist")
        logger.error(e)
        return None


def getPatientByInputs(phone, email):
    """retrieve single patient record"""
    if getPatientByPhone(phone) is not None:
        return False, f"Staff with same phone already exists: {phone}"

    if getPatientByEmail(email) is not None:
        return False, f"Staff with email already exists: {email}"

    return True, "success"


def createPatient(firstname, lastname, email, phone, password, birthday):
    """creating new patient"""
    try:
        patient = Patient.objects.create(
            id=int(str(uuid.uuid4().int)[::6]),
            first_name=firstname,
            last_name=lastname,
            phone=phone,
            email=email,
            password=make_password(password),
            birthday=birthday
        )
        return patient, "success"

    except Exception as e:
        logger.error(
            "createPatient@Error :: Error occurred while creating the patient")
        logger.error(e)
        return None, str(e)

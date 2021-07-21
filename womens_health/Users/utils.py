import uuid
import secrets
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from .models import Patient
from datetime import timedelta
from django.utils import timezone


def getExpiresAt(minutes=None):
    if not minutes:
        return (timezone.now() + timedelta(minutes=eval(settings.DURATION)))
    
    return (timezone.now() + timedelta(minutes=minutes))
from django.db import models
from Users.models import Patient

class PeriodInfo(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    cycle_average = models.TextField(null=True)
    period_average = models.TextField(null=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True)
    last_period_date = models.DateField(null=True)

    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
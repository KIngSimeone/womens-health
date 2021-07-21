from django.db import models
from django.utils.timezone import now


class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    phone = models.TextField()
    address = models.TextField(null=True)
    gender = models.TextField(null=True, max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField(null=True)
    password = models.TextField()
    image = models.TextField(null=True)

    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
    last_active_on = models.DateTimeField("last_active_on", default=now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

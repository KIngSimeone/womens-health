from django.db import models
from django.utils.timezone import now


class Patient(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    phone = models.TextField()
    address = models.TextField(null=True)
    birthday = models.DateField(null=True)
    password = models.TextField()

    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
    last_active_on = models.DateTimeField("last_active_on", default=now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserAccessTokens(models.Model):
    user_id = models.TextField(null=True)
    access_token = models.TextField("access_token")

    expires_at = models.DateTimeField("expires_at")
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)

    class Meta:
        verbose_name = "User Access Token"
        verbose_name_plural = "User Access Tokens"

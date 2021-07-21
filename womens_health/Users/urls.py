from django.urls import path

from . import routers

urlpatterns = [
    path('/patient',routers.patient_router)
]

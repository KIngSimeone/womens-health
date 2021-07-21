from django.urls import path

from . import routers

urlpatterns = [
    path('',routers.patient_router)
]

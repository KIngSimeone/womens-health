from django.urls import path

from . import routers

urlpatterns = [
    path('', routers.routers.patient_router),

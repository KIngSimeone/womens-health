from django.urls import path

from . import routers

urlpatterns = [
    path('/create-cycle',routers.cycle_router)
]

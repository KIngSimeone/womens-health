from django.urls import path

from . import routers

urlpatterns = [
    path('/create-cycles',routers.cycle_router)
]

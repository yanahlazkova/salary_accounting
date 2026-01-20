from django.urls import path

from settings.views import *

urlpatterns = [
    path('', settings, name='settings'),
]
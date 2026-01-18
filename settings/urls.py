from django.urls import path

from settings.views import *

urlpatterns = [
    path('', settings, name='settings'),
    path('new/', add_social_settings, name='add_social_settings'),
]
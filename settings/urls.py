from django.urls import path

from settings.views import *

urlpatterns = [
    path('', settings, name='settings'),
    path('/new_social_settings/', add_social_settings, name='add_social_settings'),
]
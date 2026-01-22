from django.urls import path

from settings.views import *

urlpatterns = [
    path('', settings, name='settings'),
    path('new/', add_social_settings, name='add_social_settings'),
    path('edit/<int:id_social_settings>/', edit_social_settings, name='editing'),
    path('view/<int:id_social_settings>/', view_social_settings, name='view'),
]
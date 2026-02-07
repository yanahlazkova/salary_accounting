from django.urls import path

from settings.views import *
from settings.views1 import *

app_name = 'settings'

urlpatterns = [
    # path('', settings, name='settings'),
    path('', SocialSettingsList.as_view(), name='social_settings'),
    path('new/', add_social_settings, name='create_social_settings'),
    path('edit/<int:pk>/', edit_social_settings, name='edit_social_settings'),
    path('view/<int:pk>/', SocialSettingsDetailView.as_view(), name='view_social_settings'),
#     path('view/<int:pk>/', save_social_settings, name='save'),
]
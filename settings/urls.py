from django.urls import path

from settings.views import detail
from settings.views.list import SocialSettingsListView

from settings.views1 import *

app_name = 'settings'

urlpatterns = [
    # path('', settings, name='settings'),
    path('', SocialSettingsListView.as_view(), name='social_settings'),
    path('new/', add_social_settings, name='create'),
    path('edit/<int:pk>/', edit_social_settings, name='edit'),
    path('views/<int:pk>/', detail.SocialSettingsDetailView.as_view(), name='view'),
#     path('views/<int:pk>/', save_social_settings, name='save'),
]
from django.urls import path

from settings.views import *
from settings.views1 import *

urlpatterns = [
    # path('', settings, name='settings'),
    path('', SocialSettingsListView.as_view(), name='settings'),
#     path('new/', add_social_settings, name='add_social_settings'),
    path('edit/<int:pk>/', edit_social_settings, name='edit'),
    path('view/<int:pk>/', view_social_settings, name='view'),
#     path('view/<int:pk>/', save_social_settings, name='save'),
]
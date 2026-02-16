from django.urls import path
from settings.views import detail
from settings.views.list import SocialSettingsListView

from settings.views1 import *

app_name = 'settings'

urlpatterns = [
    # path('', settings, name='settings'),
    path('', SocialSettingsListView.as_view(), name='social_settings'),
    path('new/', add_social_settings, name='create'),
    path('edit/<slug:date>/', detail.EditSocialSettings.as_view(), name='edit'),
    path('view/<slug:date>/', detail.ShowSocialSettings.as_view(), name='view'),
    # path('views/<int:pk>/', detail.ShowSocialSettings.as_view(), name='view'),
#     path('views/<int:pk>/', save_social_settings, name='save'),
]
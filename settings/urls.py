from django.urls import path
from settings.views import list, detail, edit

from settings.views1 import *

app_name = 'settings'

urlpatterns = [
    # path('', settings, name='settings'),
    path('', list.SocialSettingsListView.as_view(), name='social_settings'),
    path('new/', add_social_settings, name='create'),
    path('view/<slug:date>/', detail.ShowSocialSettings.as_view(), name='view'),
    path('edit/<slug:date>/', edit.EditSocialSettings.as_view(), name='edit'),
    # path('views/<int:pk>/', detail.ShowSocialSettings.as_view(), name='view'),
#     path('views/<int:pk>/', update, name='update'),
]
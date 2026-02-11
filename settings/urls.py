from django.urls import path

from settings import views_now
from settings.views.list import SocialSettingsListView

from settings.views1 import *

app_name = 'settings'

urlpatterns = [
    # path('', settings, name='settings'),
    path('', SocialSettingsListView.as_view(), name='social_settings'),
    path('new/', add_social_settings, name='create_social_settings'),
    path('edit/<int:pk>/', edit_social_settings, name='edit_social_settings'),
    path('views/<int:pk>/', views_now.SocialSettingsDetailView.as_view(), name='view_social_settings'),
#     path('views/<int:pk>/', save_social_settings, name='save'),
]

from django.urls import path
from settings.views import list, detail, edit, create, copy
from settings.views.create import CreateSocialSettingsView

from settings.views1 import *

app_name = 'settings'

urlpatterns = [
    # path('', settings, name='settings'),
    path('', list.SocialSettingsListView.as_view(), name='social_settings'),
    path('new/', create.CreateSocialSettingsView.as_view(), name='create'),
    path('view/<slug:date>/', detail.ShowSocialSettingsView.as_view(), name='view'),
    path('edit/<slug:date>/', edit.EditSocialSettingsView.as_view(), name='edit'),
    path('views/<slug:date>/', copy.CopySocialSettingsView.as_view(), name='copy'),
#     path('views/<int:pk>/', update, name='update'),
]
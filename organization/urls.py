from django.urls import path

from organization.views.dashboard import DashboardOrgView
from organization.views1 import SettingsOrgEditView, SettingsOrgCreateView, SettingsUstanovaCreateView

app_name = 'organization'

urlpatterns = [
    # path('', SettingsOrgView.as_view(), name='settings'),
    path('', DashboardOrgView.as_view(), name='settings'),
    path('edit_org/<slug:edrpou>', SettingsOrgEditView.as_view(), name='edit_org'),
    path('create_org/', SettingsOrgCreateView.as_view(), name='create_org'),
    path('create_ustanova/', SettingsUstanovaCreateView.as_view(), name='create'),

]

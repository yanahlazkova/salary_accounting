from django.urls import path

from organization.views.create import SettingsOrgCreateView
from organization.views.dashboard import DashboardOrgView
from organization.views.edit import SettingsOrgEditView
from organization.views1 import SettingsUstanovaCreateView, SettingsUstanovaDetailView, SettingsUstanovaEditView

# from organization.views.create import SettingsOrgCreateView, SettingsUstanovaCreateView
# from organization.views.dashboard import DashboardOrgView
# from organization.views.edit import SettingsOrgEditView

app_name = 'organization'

urlpatterns = [
    # path('', SettingsOrgView.as_view(), name='settings'),
    path('', DashboardOrgView.as_view(), name='settings'),
    path('edit_org/<slug:edrpou>', SettingsOrgEditView.as_view(), name='edit_org'),
    path('new_org/', SettingsOrgCreateView.as_view(), name='create_org'),
    path('new_ustanova/', SettingsUstanovaCreateView.as_view(), name='create_ust'),
    path('ustanovy/<slug:kpk>', SettingsUstanovaDetailView.as_view(), name='view_ust'),
    path('ustanovy/<slug:kpk>/edit/', SettingsUstanovaEditView.as_view(), name='edit_ust'),

]

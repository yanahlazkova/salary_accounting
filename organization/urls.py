from django.urls import path

from organization.views.create import SettingsOrgCreateView, SettingsUstanovaCreateView, BankAccountCreateView
from organization.views.dashboard import DashboardOrgView
from organization.views.detail import SettingsUstanovaDetailView
from organization.views.edit import SettingsOrgEditView, SettingsUstanovaEditView, BankAccountEditView
from ui.views.detail_account import BankAccountDetailView


app_name = 'organization'

urlpatterns = [
    path('', DashboardOrgView.as_view(), name='settings'),
    path('edit_org/<slug:edrpou>', SettingsOrgEditView.as_view(), name='edit_org'),
    path('new_org/', SettingsOrgCreateView.as_view(), name='create_org'),
    path('new_ustanova/', SettingsUstanovaCreateView.as_view(), name='create_ust'),
    path('ustanova/<slug:kpk>', SettingsUstanovaDetailView.as_view(), name='view_ust'),
    path('ustanova/edit/<slug:kpk>/', SettingsUstanovaEditView.as_view(), name='edit_ust'),
    path('ustanova/account/edit/<slug:account>', BankAccountEditView.as_view(), name='edit_account'),
    path('<slug:ustanova_kpk>/new-account/', BankAccountCreateView.as_view(), name='create_account'),
    # path('ustanova/account/new/<slug:kpk>/', BankAccountCreateView.as_view(), name='create_account'),
    path('ustanova/account/<slug:account>', BankAccountDetailView.as_view(), name='view_account'),

]

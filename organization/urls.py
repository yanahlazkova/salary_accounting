from django.urls import path

from organization.views.create import SettingsOrgCreateView, SettingsUstanovaCreateView, BankAccountCreateView, \
    DepartmentCreateView
from organization.views.dashboard import DashboardOrgView
from organization.views.detail import SettingsUstanovaDetailView
from organization.views.detail_department import DepartmentDetailView
from organization.views.edit import SettingsOrgEditView, SettingsUstanovaEditView, BankAccountEditView, \
    DepartmentEditView
from organization.views.detail_account import BankAccountDetailView


app_name = 'organization'

urlpatterns = [
    path('', DashboardOrgView.as_view(), name='settings'),
    path('edit_org/<slug:edrpou>', SettingsOrgEditView.as_view(), name='edit_org'),
    path('new_org/', SettingsOrgCreateView.as_view(), name='create_org'),
    path('new_ustanova/', SettingsUstanovaCreateView.as_view(), name='create_ust'),
    path('ustanova/<slug:kpk>', SettingsUstanovaDetailView.as_view(), name='view_ust'),
    path('ustanova/edit/<slug:kpk>/', SettingsUstanovaEditView.as_view(), name='edit_ust'),

    path('ustanova/account/edit/<slug:account>', BankAccountEditView.as_view(), name='edit_account'),
    path('<slug:kpk>/new-account/', BankAccountCreateView.as_view(), name='create_account'),
    path('ustanova/account/<slug:account>', BankAccountDetailView.as_view(), name='view_account'),

    path('ustanova/department-new/<slug:kpk>', DepartmentCreateView.as_view(), name='create_department'),
    path('ustanova/department/<slug:pk>', DepartmentDetailView.as_view(), name='view_department'),
    path('ustanova/department-edit/<slug:pk>', DepartmentEditView.as_view(), name='edit_department'),

]

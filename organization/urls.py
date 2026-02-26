from django.urls import path

from organization import views

app_name = 'organization'

urlpatterns = [
    path('', views.SettingsOrgView.as_view(), name='settings'),
    path('edit_org/', views.SettingsOrgEditView.as_view(), name='edit_org'),

]

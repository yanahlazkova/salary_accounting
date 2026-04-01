from django.urls import path

from pharmacy import views
from pharmacy.views import PharmacyView, PharmacyBasePageView

app_name = 'pharmacy'

urlpatterns = [
    path('', PharmacyBasePageView.as_view(), name='pharmacy'),
]